"""The retry table in action: what the client sends again, when, and when it stops.

Every case sends a post through Status200.publish() on a scripted transport, so the tests see the
real requests (their bodies and Idempotency-Keys) and the waits the client asked for."""

from __future__ import annotations

import httpx
import pytest
from conftest import error_reply, json_reply, page_reply

from status200uploads import RETRY_TABLE, OutcomeUnknown, Status200Error, retry_rule
from status200uploads._retry import DEFAULT_WAIT_SECONDS, UNAVAILABLE_CODES, UNAVAILABLE_RESENDS

POST = {"accountId": "@myprofile", "platform": "x", "content": {"text": "Hello"}}
OK = {"data": {"tweet_id": "1", "url": "https://x.com/i/status/1"}}


def ok() -> httpx.Response:
    return json_reply(200, OK)


class TestRetryRule:
    def test_code_first_then_status_class_then_not_json(self) -> None:
        assert retry_rule(409, "media_processing") == "wait_and_resend"
        assert retry_rule(409, "not_cancellable") == "never"
        assert retry_rule(500, "something_new") == "resend_once_with_key"
        assert retry_rule(202, "still_publishing") == "not_a_failure"
        assert retry_rule(200) == "not_a_failure"
        assert retry_rule(504, json=False) == "resend_once_with_key"
        assert retry_rule(0, json=False) == "resend_once_with_key"
        assert retry_rule(302) == "never"

    def test_a_code_of_another_type_or_an_attribute_name_is_not_read(self) -> None:
        assert retry_rule(400, "__class__") == "never"
        assert retry_rule(400, None) == "never"

    def test_the_unavailable_codes_are_wait_and_resend_codes(self) -> None:
        for code in UNAVAILABLE_CODES:
            assert RETRY_TABLE["by_code"][code] == "wait_and_resend", code


class TestEvery2xxIsASuccess:
    @pytest.mark.parametrize(
        ("status", "body"),
        [
            (200, OK),
            (200, {"dry_run": True, "outcome": "refuse"}),
            (202, {"code": "scheduled", "scheduled_post_id": "x"}),
            (202, {"code": "queued_for_next_day"}),
            (
                202,
                {"success": False, "status": "unknown", "code": "still_publishing", "retry": False},
            ),
            (
                202,
                {
                    "success": False,
                    "status": "unknown",
                    "code": "schedule_unconfirmed",
                    "retry": False,
                },
            ),
            (202, {"data": {"status": "processing", "job_id": "j"}}),
        ],
    )
    def test_never_sent_again(self, make_client, sleeps, status, body) -> None:
        client, script = make_client(json_reply(status, body))
        result = client.publish(POST)
        assert result.status_code == status
        assert result.raw == body
        assert len(script.requests) == 1
        assert sleeps == []


class TestWaitAndResend:
    def test_waits_retry_after_then_sends_the_identical_request(self, make_client, sleeps) -> None:
        client, script = make_client(
            error_reply(
                409, "media_processing", {"retry_after_seconds": 30}, {"Retry-After": "30"}
            ),
            ok(),
        )
        result = client.publish(POST)
        assert result.status_code == 200
        assert result.tries == 2
        assert sleeps == [30]
        first, second = script.requests
        assert first.content == second.content
        assert first.headers["idempotency-key"] == second.headers["idempotency-key"]
        assert result.idempotency_key == first.headers["idempotency-key"]

    def test_the_retry_after_header_comes_first(self, make_client, sleeps) -> None:
        client, _ = make_client(
            error_reply(429, "rate_limited", {"retry_after_seconds": 9}, {"Retry-After": "7"}),
            ok(),
        )
        client.publish(POST)
        assert sleeps == [7]

    def test_retry_after_seconds_when_there_is_no_header_else_5_seconds(
        self, make_client, sleeps
    ) -> None:
        client, _ = make_client(error_reply(429, "rate_limited", {"retry_after_seconds": 17}), ok())
        client.publish(POST)
        client2, _ = make_client(error_reply(409, "idempotency_in_progress"), ok())
        client2.publish(POST)
        assert sleeps == [17, DEFAULT_WAIT_SECONDS]

    def test_a_retry_after_of_0_waits_1_second(self, make_client, sleeps) -> None:
        client, _ = make_client(error_reply(429, "rate_limited", {}, {"Retry-After": "0"}), ok())
        client.publish(POST)
        assert sleeps == [1]

    def test_never_waits_past_max_wait_in_all(self, make_client, sleeps) -> None:
        def busy() -> httpx.Response:
            return error_reply(
                409, "media_processing", {"retry_after_seconds": 30}, {"Retry-After": "30"}
            )

        client, script = make_client(busy(), busy(), busy(), busy(), max_wait=100, max_tries=10)
        with pytest.raises(Status200Error) as raised:
            client.publish(POST)
        assert sleeps == [30, 30, 30]
        assert len(script.requests) == 4
        error = raised.value
        assert type(error) is Status200Error  # nothing was sent: not an unknown outcome
        assert (error.reason, error.code, error.status) == ("max_wait", "media_processing", 409)
        assert error.retry_after_seconds == 30
        assert error.waited_seconds == 90
        assert "max_wait (100 s)" in str(error)
        # The API's sentence stays apart from what the client adds.
        assert error.message == "media_processing message"
        assert "max_wait (100 s)" in error.note

    def test_a_wait_longer_than_max_wait_is_not_waited_at_all(self, make_client, sleeps) -> None:
        client, script = make_client(
            error_reply(429, "rate_limited", {"retry_after_seconds": 86000})
        )
        with pytest.raises(Status200Error) as raised:
            client.publish(POST, max_wait=600)
        assert raised.value.reason == "max_wait"
        assert raised.value.retry_after_seconds == 86000
        assert sleeps == []
        assert len(script.requests) == 1

    def test_max_wait_0_never_waits_and_says_how_long_to_wait(self, make_client, sleeps) -> None:
        client, _ = make_client(error_reply(429, "rate_limited", {"retry_after_seconds": 12}))
        with pytest.raises(Status200Error) as raised:
            client.publish(POST, max_wait=0)
        assert (raised.value.reason, raised.value.retry_after_seconds) == ("max_wait", 12)
        assert sleeps == []

    @pytest.mark.parametrize("code", sorted(UNAVAILABLE_CODES))
    def test_a_nothing_was_sent_code_is_sent_again_at_most_twice(
        self, make_client, sleeps, code
    ) -> None:
        def down() -> httpx.Response:
            return error_reply(503, code, {"retry_after_seconds": 5}, {"Retry-After": "5"})

        client, script = make_client(down(), down(), down(), down())
        with pytest.raises(Status200Error) as raised:
            client.publish(POST)
        assert UNAVAILABLE_RESENDS == 2  # "at most twice", as the README and the n8n node say
        assert len(script.requests) == 3
        assert raised.value.reason == "tries_used"

    def test_never_more_than_max_tries_requests(self, make_client, sleeps) -> None:
        def busy() -> httpx.Response:
            return error_reply(409, "idempotency_in_progress", {}, {"Retry-After": "1"})

        client, script = make_client(*[busy() for _ in range(10)], max_tries=5, max_wait=600)
        with pytest.raises(OutcomeUnknown) as raised:
            client.publish(POST)
        # The first request with this key is still running: it may still go through.
        assert len(script.requests) == 5
        assert (raised.value.reason, raised.value.tries) == ("tries_used", 5)

    def test_the_media_shape_is_read_too(self, make_client, sleeps) -> None:
        # /api/v2/media's 429: the sentence in "error", its code and wait next to it.
        client, script = make_client(
            json_reply(
                429,
                {"error": "Please wait", "code": "rate_limited", "retry_after_seconds": 12},
                {"Retry-After": "12"},
            ),
            json_reply(200, {"success": True, "file_id": "f", "status": "ready"}),
        )
        media = client.import_media("https://example.com/a.jpg")
        assert media["status"] == "ready"
        assert sleeps == [12]
        assert script.requests[0].content == script.requests[1].content


class TestResendOnceWithKey:
    def test_with_a_key_one_more_try_after_retry_after_or_5_seconds(
        self, make_client, sleeps
    ) -> None:
        replayed = json_reply(200, OK, {"Idempotent-Replayed": "true"})
        client, script = make_client(page_reply(504), replayed)
        result = client.publish(POST)
        assert result.replayed is True
        assert sleeps == [5]
        assert len(script.requests) == 2
        assert script.requests[0].content == script.requests[1].content
        assert (
            script.requests[0].headers["idempotency-key"]
            == script.requests[1].headers["idempotency-key"]
        )

    def test_no_answer_at_all_is_sent_once_more_with_the_key(self, make_client, sleeps) -> None:
        client, script = make_client(httpx.ReadTimeout("timed out"), ok())
        result = client.publish(POST)
        assert result.tries == 2
        assert len(script.requests) == 2

    def test_with_a_key_only_once(self, make_client, sleeps) -> None:
        client, script = make_client(
            error_reply(500, "server_error"), error_reply(500, "server_error"), ok()
        )
        with pytest.raises(OutcomeUnknown) as raised:
            client.publish(POST)
        assert len(script.requests) == 2
        error = raised.value
        assert (error.reason, error.code, error.status) == ("once_used", "server_error", 500)
        assert error.idempotency_key is not None
        assert "same idempotency_key" in str(error)

    @pytest.mark.parametrize(
        "first",
        [
            lambda: error_reply(500, "platform_error"),
            lambda: httpx.ConnectError("connection refused"),
            lambda: httpx.Response(502, text="Bad Gateway"),
        ],
    )
    def test_without_a_key_not_sent_again(self, make_client, sleeps, first) -> None:
        client, script = make_client(first(), ok())
        with pytest.raises(OutcomeUnknown) as raised:
            client.publish(POST, idempotency_key=False)
        assert raised.value.reason == "no_key"
        assert len(script.requests) == 1
        assert "idempotency-key" not in script.requests[0].headers
        assert sleeps == []

    def test_a_dry_run_is_sent_again_once_without_a_key(self, make_client, sleeps) -> None:
        client, script = make_client(
            error_reply(500, "server_error"), json_reply(200, {"dry_run": True})
        )
        result = client.publish(POST, dry_run=True, idempotency_key=False)
        assert result.dry_run is True
        assert len(script.requests) == 2

    def test_a_read_is_sent_again_once_and_its_failure_is_not_an_unknown_outcome(
        self, make_client, sleeps
    ) -> None:
        client, script = make_client(
            error_reply(500, "server_error"), error_reply(500, "server_error")
        )
        with pytest.raises(Status200Error) as raised:
            client.list_accounts()
        assert type(raised.value) is Status200Error
        assert raised.value.reason == "once_used"
        assert len(script.requests) == 2

    def test_is_not_bound_by_max_wait(self, make_client, sleeps) -> None:
        # One short pause after a lost answer, not a wait the API asked for.
        client, _ = make_client(httpx.ReadTimeout("timed out"), ok(), max_wait=0)
        assert client.publish(POST).status_code == 200


class TestNever:
    def test_stops_at_once_on_every_code_the_table_marks_never_and_any_other_4xx(
        self, make_client, sleeps
    ) -> None:
        never = [code for code, rule in RETRY_TABLE["by_code"].items() if rule == "never"]
        for code in [*never, "bad_request", "account_not_found", "not_cancellable", "a_new_code"]:
            client, script = make_client(error_reply(422, code), ok())
            with pytest.raises(Status200Error) as raised:
                client.publish(POST)
            assert raised.value.reason == "refused", code
            assert len(script.requests) == 1, code
        assert sleeps == []

    def test_idempotency_outcome_unknown_is_an_unknown_outcome_that_a_new_key_may_resend(
        self, make_client, sleeps
    ) -> None:
        client, script = make_client(error_reply(409, "idempotency_outcome_unknown"), ok())
        with pytest.raises(OutcomeUnknown) as raised:
            client.publish(POST)
        assert len(script.requests) == 1
        assert "new idempotency_key only if it is not there" in str(raised.value)

    def test_an_accepted_code_on_a_status_that_is_not_2xx_contradicts_itself(
        self, make_client, sleeps
    ) -> None:
        client, script = make_client(error_reply(400, "scheduled"), ok())
        with pytest.raises(Status200Error):
            client.publish(POST)
        assert len(script.requests) == 1

    def test_a_refusal_carries_the_apis_code_message_and_facts(self, make_client, sleeps) -> None:
        client, _ = make_client(
            error_reply(
                403,
                "plan_required",
                {
                    "required": "x_addon",
                    "platform": "x",
                    "plan": "free",
                    "upgrade_url": "https://status200uploads.com/pricing",
                },
            )
        )
        with pytest.raises(Status200Error) as raised:
            client.publish(POST)
        error = raised.value
        assert (error.status, error.code, error.message) == (
            403,
            "plan_required",
            "plan_required message",
        )
        assert error.upgrade_url == "https://status200uploads.com/pricing"
        assert error.details["required"] == "x_addon"
        assert error.rule == "never"
        assert str(error) == "plan_required message [HTTP 403, code plan_required]"
        # REST refusals carry no next_step and no retry rule: the error does not invent them.
        assert not hasattr(error, "next_step")

    def test_a_failure_that_left_a_post_in_history_names_it(self, make_client, sleeps) -> None:
        ids = {
            "post_id": "e5f6a7b8-c9d0-1234-ef01-345678901234",
            "scheduled_post_id": None,
            "status_url": "https://status200uploads.com/api/v2/posts/e5f6a7b8-c9d0-1234-ef01-345678901234",
        }
        client, _ = make_client(
            json_reply(
                422,
                {"error": {"code": "x_rejected", "message": "X said no"}, "status200": ids},
            )
        )
        with pytest.raises(Status200Error) as raised:
            client.publish(POST)
        assert raised.value.status200 is not None
        assert raised.value.status200.post_id == ids["post_id"]
