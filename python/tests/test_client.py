"""Status200 on a scripted transport: the requests it builds, what it returns, how it waits, and
that the API key never shows."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime, timedelta, timezone

import httpx
import pytest
from conftest import TEST_KEY, error_reply, json_reply, response_examples

from status200uploads import (
    DEFAULT_BASE_URL,
    USER_AGENT,
    Result,
    Status200,
    Status200Error,
    Status200Ids,
    __version__,
)
from status200uploads.models import Post, PostContent, PostRequest, TikTokOptions

POST_ID = "b2c3d4e5-f6a7-8901-bcde-f12345678901"
SCHEDULED_ID = "c3d4e5f6-a7b8-9012-cdef-123456789012"
PROFILE_ID = "d4e5f6a7-b8c9-0123-def0-234567890123"
FILE_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
POST = {"accountId": "@myprofile", "platform": "linkedin", "content": {"text": "Hello"}}


def body_of(request: httpx.Request) -> dict:
    return json.loads(request.content)


def post_read(status: str, done: bool, **extra) -> httpx.Response:
    return json_reply(
        200,
        {
            "data": {
                "id": POST_ID,
                "kind": "post",
                "status": status,
                "done": done,
                "permalink": None,
                **extra,
            }
        },
    )


class TestSetup:
    def test_the_key_comes_from_the_argument_or_the_environment(self, monkeypatch) -> None:
        monkeypatch.delenv("STATUS200_API_KEY", raising=False)
        with pytest.raises(ValueError, match="STATUS200_API_KEY"):
            Status200()
        with pytest.raises(ValueError, match="No API key"):
            Status200(api_key="   ")
        monkeypatch.setenv("STATUS200_API_KEY", TEST_KEY)
        with Status200() as client:
            assert client._http.headers["authorization"] == f"Bearer {TEST_KEY}"

    def test_defaults_base_url_timeout_user_agent(self) -> None:
        with Status200(api_key=TEST_KEY) as client:
            assert client.base_url == DEFAULT_BASE_URL == "https://status200uploads.com/api/v2"
            timeout = client._http.timeout
            assert (timeout.connect, timeout.read, timeout.write, timeout.pool) == (
                10,
                120,
                120,
                120,
            )
            assert client._http.headers["user-agent"] == USER_AGENT
            assert USER_AGENT == f"status200uploads-python/{__version__}"
            assert client._http.follow_redirects is False

    def test_a_number_is_a_timeout_in_seconds(self) -> None:
        with Status200(api_key=TEST_KEY, timeout=30) as client:
            assert client._http.timeout.read == 30

    def test_an_httpx_timeout_or_none_is_used_as_it_is(self) -> None:
        with Status200(api_key=TEST_KEY, timeout=httpx.Timeout(7, connect=2)) as client:
            assert (client._http.timeout.connect, client._http.timeout.read) == (2, 7)
        with Status200(api_key=TEST_KEY, timeout=None) as client:
            assert client._http.timeout.read is None

    def test_true_or_false_is_not_a_timeout(self) -> None:
        with pytest.raises(TypeError, match="timeout"):
            Status200(api_key=TEST_KEY, timeout=True)

    def test_every_request_carries_the_key_the_user_agent_and_json(self, make_client) -> None:
        client, script = make_client(json_reply(200, {"data": []}))
        client.list_accounts()
        request = script.requests[0]
        assert str(request.url) == "https://status200uploads.com/api/v2/accounts"
        assert request.headers["authorization"] == f"Bearer {TEST_KEY}"
        assert request.headers["user-agent"] == USER_AGENT
        assert request.headers["accept"] == "application/json"

    def test_the_key_never_shows(self, make_client, caplog) -> None:
        caplog.set_level(logging.DEBUG, logger="status200uploads")
        client, _ = make_client(
            error_reply(429, "rate_limited", {"retry_after_seconds": 1}),
            error_reply(401, "unauthorized"),
        )
        with pytest.raises(Status200Error) as raised:
            client.publish(POST)
        shown = [
            repr(client),
            str(client),
            repr(client.client),
            str(client._http.headers),
            repr(client._http.headers),
            str(raised.value),
            repr(raised.value),
            str(raised.value.details),
            str(raised.value.headers),
            caplog.text,
        ]
        for text in shown:
            assert TEST_KEY not in text
        # The generated client keeps its safe repr after attrs' evolve (with_headers, with_timeout).
        assert "[hidden]" in repr(client.client.with_headers({"X-Test": "1"}))


class TestPublish:
    def test_a_post_dict_is_sent_as_the_request_body(self, make_client) -> None:
        client, script = make_client(json_reply(200, {"data": {"post_id": "urn:li:share:1"}}))
        client.publish(POST)
        request = script.requests[0]
        assert (request.method, str(request.url)) == (
            "POST",
            "https://status200uploads.com/api/v2/posts",
        )
        assert request.headers["content-type"] == "application/json"
        assert body_of(request) == {"post": POST}

    def test_a_whole_request_and_generated_models_work_too(self, make_client) -> None:
        client, script = make_client(*[json_reply(200, {"data": {}}) for _ in range(3)])
        client.publish({"post": POST, "dryRun": False})
        client.publish(
            Post(
                account_id="@myprofile",
                platform="tiktok",
                content=PostContent(text="New video", media_id=[FILE_ID]),
                tiktok=TikTokOptions(privacy_level="PUBLIC_TO_EVERYONE"),
            )
        )
        client.publish(PostRequest(post=Post(account_id="@myprofile", platform="x")))
        first, second, third = (body_of(r) for r in script.requests)
        assert first == {"post": POST, "dryRun": False}
        assert second["post"]["accountId"] == "@myprofile"
        assert second["post"]["content"] == {"text": "New video", "mediaID": [FILE_ID]}
        assert second["post"]["tiktok"]["privacyLevel"] == "PUBLIC_TO_EVERYONE"
        assert third == {"post": {"accountId": "@myprofile", "platform": "x"}}

    def test_the_callers_dict_is_not_changed(self, make_client) -> None:
        client, _ = make_client(json_reply(202, {"code": "scheduled"}))
        post = {"accountId": "@myprofile", "platform": "x", "content": {"text": "Later"}}
        client.publish(post, scheduled_for="2026-10-01T09:00:00Z", dry_run=False)
        assert post == {"accountId": "@myprofile", "platform": "x", "content": {"text": "Later"}}

    def test_every_post_gets_its_own_automatic_key(self, make_client) -> None:
        client, script = make_client(json_reply(200, {"data": {}}), json_reply(200, {"data": {}}))
        first = client.publish(POST)
        second = client.publish(POST)
        keys = [r.headers["idempotency-key"] for r in script.requests]
        assert keys == [first.idempotency_key, second.idempotency_key]
        assert keys[0] != keys[1]
        for key in keys:
            uuid.UUID(key)

    def test_your_own_key_or_none(self, make_client) -> None:
        client, script = make_client(json_reply(200, {"data": {}}), json_reply(200, {"data": {}}))
        client.publish(POST, idempotency_key="  order-1234-linkedin ")
        client.publish(POST, idempotency_key=False)
        assert script.requests[0].headers["idempotency-key"] == "order-1234-linkedin"
        assert "idempotency-key" not in script.requests[1].headers

    @pytest.mark.parametrize(
        ("given", "sent"),
        [
            ("\tK\t", "K"),
            ("ok\n", "ok"),
            ('"K"', "K"),
            (' "order 7" ', "order 7"),
            ('""K""', '"K"'),
            ('"', '"'),
            (" K﻿", "K"),
        ],
    )
    def test_a_key_is_read_exactly_as_the_api_reads_it(self, make_client, given, sent) -> None:
        # The API trims with JavaScript's trim(), then removes ONE pair of surrounding double
        # quotes; the header carries the key the API will use, and so does the result.
        client, script = make_client(json_reply(200, {"data": {}}))
        result = client.publish(POST, idempotency_key=given)
        assert script.requests[0].headers["idempotency-key"] == sent
        assert result.idempotency_key == sent

    @pytest.mark.parametrize(
        "bad", ["", "   ", '""', ' "" ', "x" * 256, "café", "a\nb", "tab\there"]
    )
    def test_a_key_the_api_would_refuse_is_refused_before_sending(self, make_client, bad) -> None:
        client, script = make_client()
        with pytest.raises(ValueError, match="printable ASCII"):
            client.publish(POST, idempotency_key=bad)
        assert script.requests == []

    def test_scheduled_for_takes_a_datetime_with_a_time_zone(self, make_client) -> None:
        client, script = make_client(
            json_reply(202, {"code": "scheduled"}), json_reply(202, {"code": "scheduled"})
        )
        client.publish(POST, scheduled_for=datetime(2026, 10, 1, 9, 0, tzinfo=UTC))
        plus_two = timezone(timedelta(hours=2))
        client.publish({**POST, "scheduledFor": datetime(2026, 10, 1, 11, 0, tzinfo=plus_two)})
        assert body_of(script.requests[0])["post"]["scheduledFor"] == "2026-10-01T09:00:00+00:00"
        assert body_of(script.requests[1])["post"]["scheduledFor"] == "2026-10-01T11:00:00+02:00"

    def test_a_time_without_a_zone_is_refused_before_sending(self, make_client) -> None:
        client, script = make_client()
        with pytest.raises(ValueError, match="no time zone"):
            client.publish(POST, scheduled_for=datetime(2026, 10, 1, 9, 0))  # noqa: DTZ001
        assert script.requests == []

    def test_the_published_examples_of_the_file(self, make_client, spec) -> None:
        for name, example in response_examples(spec, "Published").items():
            client, _ = make_client(json_reply(200, example))
            result = client.publish(POST)
            assert isinstance(result, Result)
            assert result.raw == example
            assert result.accepted is False
            if name == "dryRun":
                assert result.dry_run is True
                assert result.status200 is None
            else:
                assert result.data == example["data"]
                assert result.status200 == Status200Ids(**example["status200"])

    def test_the_accepted_examples_of_the_file(self, make_client, spec) -> None:
        for name, example in response_examples(spec, "Accepted").items():
            client, script = make_client(json_reply(202, example))
            result = client.publish(POST)
            assert result.accepted is True, name
            assert result.code == example.get("code"), name
            assert result.status200 == Status200Ids(**example["status200"]), name
            assert len(script.requests) == 1

    def test_warnings_and_replays_are_reported(self, make_client) -> None:
        warning = {"code": "unknown_field", "message": "post.foo is not used", "field": "post.foo"}
        client, _ = make_client(
            json_reply(200, {"data": {}, "warnings": [warning]}, {"Idempotent-Replayed": "true"})
        )
        result = client.publish(POST, idempotency_key="k-1")
        assert result.warnings == [warning]
        assert result.replayed is True

    def test_validate_is_a_dry_run(self, make_client, spec) -> None:
        report = response_examples(spec, "Published")["dryRun"]
        client, script = make_client(json_reply(200, report))
        assert client.validate(POST) == report
        assert body_of(script.requests[0]) == {"post": POST, "dryRun": True}

    def test_wait_follows_a_post_to_its_result(self, make_client, sleeps, spec) -> None:
        processing = response_examples(spec, "Published")["tiktok"]
        client, script = make_client(
            json_reply(200, processing),
            post_read("processing", False),
            post_read("processing", False),
            post_read("success", True, permalink="https://www.tiktok.com/@me/video/1"),
        )
        result = client.publish(POST, wait=True)
        assert result.final is not None
        assert result.final["status"] == "success"
        assert result.final["permalink"] == "https://www.tiktok.com/@me/video/1"
        reads = script.requests[1:]
        assert [r.method for r in reads] == ["GET"] * 3
        assert {str(r.url) for r in reads} == {f"{DEFAULT_BASE_URL}/posts/{POST_ID}"}
        assert sleeps == [30, 30]
        # Waiting never posts again.
        assert [r.method for r in script.requests].count("POST") == 1

    def test_a_wait_that_cannot_read_the_post_does_not_fail_the_post(
        self, make_client, sleeps, spec, caplog
    ) -> None:
        # The post was accepted; raising would invite sending it again.
        processing = response_examples(spec, "Published")["tiktok"]
        client, script = make_client(
            json_reply(200, processing),
            error_reply(500, "server_error"),
            error_reply(500, "server_error"),
        )
        result = client.publish(POST, wait=True)
        assert result.status_code == 200
        assert result.final is None
        assert [r.method for r in script.requests] == ["POST", "GET", "GET"]
        assert "reading its result failed" in caplog.text

    def test_wait_does_not_follow_a_scheduled_post(self, make_client, spec) -> None:
        scheduled = response_examples(spec, "Accepted")["scheduled"]
        client, script = make_client(json_reply(202, scheduled))
        result = client.publish(POST, wait=True)
        assert result.final is None
        assert len(script.requests) == 1


class TestWaitFor:
    def test_reads_every_30_seconds_for_at_most_10_minutes(self, make_client, sleeps) -> None:
        client, script = make_client(*[post_read("processing", False) for _ in range(25)])
        last = client.wait_for(POST_ID)
        assert last["status"] == "processing"  # the last state, not an error
        assert len(script.requests) == 20
        assert sleeps == [30] * 19

    def test_stops_as_soon_as_done(self, make_client, sleeps) -> None:
        client, script = make_client(post_read("failed", True, error_message="X said no"))
        assert client.wait_for(POST_ID)["status"] == "failed"
        assert len(script.requests) == 1
        assert sleeps == []

    def test_a_status_url_is_read_at_this_clients_address_only(self, make_client, sleeps) -> None:
        client, script = make_client(post_read("success", True))
        client.wait_for(f"https://elsewhere.example/api/v2/posts/{POST_ID}/")
        assert str(script.requests[0].url) == f"{DEFAULT_BASE_URL}/posts/{POST_ID}"

    def test_a_status_url_with_a_query_is_read_by_its_id(self, make_client, sleeps) -> None:
        client, script = make_client(post_read("success", True))
        client.wait_for(f"{DEFAULT_BASE_URL}/posts/{POST_ID}?utm=1#top")
        assert str(script.requests[0].url) == f"{DEFAULT_BASE_URL}/posts/{POST_ID}"

    def test_takes_a_result_or_its_ids(self, make_client, sleeps, spec) -> None:
        example = response_examples(spec, "Published")["x"]
        client, script = make_client(post_read("success", True), post_read("success", True))
        result = Result(200, example, {}, False, None, 1)
        client.wait_for(result)
        client.wait_for(result.status200)
        post_id = example["status200"]["post_id"]
        assert [str(r.url) for r in script.requests] == [f"{DEFAULT_BASE_URL}/posts/{post_id}"] * 2

    @pytest.mark.parametrize("target", ["../accounts", "not-an-id", "", "https://x/posts/"])
    def test_anything_but_a_post_id_is_refused_before_sending(self, make_client, target) -> None:
        client, script = make_client()
        with pytest.raises(ValueError, match="UUID"):
            client.wait_for(target)
        assert script.requests == []

    def test_a_dry_run_has_nothing_to_wait_for(self, make_client) -> None:
        client, _ = make_client()
        with pytest.raises(ValueError, match="dry run"):
            client.wait_for(Result(200, {"dry_run": True}, {}, False, None, 1))


class TestReads:
    def test_accounts(self, make_client) -> None:
        accounts = [{"profile_id": PROFILE_ID, "handle": "@myprofile", "networks": []}]
        client, script = make_client(json_reply(200, {"data": accounts}))
        assert client.list_accounts() == accounts
        assert script.requests[0].method == "GET"

    def test_posting_options(self, make_client) -> None:
        data = {"profile_id": PROFILE_ID, "networks": []}
        client, script = make_client(json_reply(200, {"data": data}))
        assert client.get_posting_options(PROFILE_ID, platforms=["tiktok", "pinterest"]) == data
        url = script.requests[0].url
        assert url.path == f"/api/v2/accounts/{PROFILE_ID}/options"
        assert url.params["platforms"] == "tiktok,pinterest"

    def test_list_posts_filters(self, make_client) -> None:
        page = {"data": [], "next_cursor": None, "next_url": None}
        client, script = make_client(json_reply(200, page))
        got = client.list_posts(
            limit=50, status=["success", "failed"], platform="x", kind="post", profile_id=PROFILE_ID
        )
        assert got == page
        assert dict(script.requests[0].url.params) == {
            "limit": "50",
            "status": "success,failed",
            "platform": "x",
            "kind": "post",
            "profile_id": PROFILE_ID,
        }

    def test_iter_posts_follows_the_cursor(self, make_client) -> None:
        client, script = make_client(
            json_reply(
                200, {"data": [{"id": "1"}, {"id": "2"}], "next_cursor": "c2", "next_url": "u"}
            ),
            json_reply(200, {"data": [{"id": "3"}], "next_cursor": None, "next_url": None}),
        )
        assert [p["id"] for p in client.iter_posts(platform="x")] == ["1", "2", "3"]
        assert "cursor" not in script.requests[0].url.params
        assert script.requests[1].url.params["cursor"] == "c2"
        assert script.requests[1].url.params["limit"] == "100"

    def test_iter_posts_stops_on_a_cursor_it_has_seen(self, make_client) -> None:
        page = {"data": [{"id": "1"}], "next_cursor": "same", "next_url": "u"}
        client, script = make_client(json_reply(200, page), json_reply(200, page))
        assert [p["id"] for p in client.iter_posts()] == ["1", "1"]
        assert len(script.requests) == 2

    def test_a_read_waits_out_the_read_limit(self, make_client, sleeps) -> None:
        client, script = make_client(
            error_reply(429, "rate_limited", {"limit": 60}, {"Retry-After": "7"}),
            json_reply(200, {"data": []}),
        )
        assert client.list_accounts() == []
        assert sleeps == [7]
        assert len(script.requests) == 2

    def test_a_missing_post_is_a_refusal(self, make_client) -> None:
        client, _ = make_client(error_reply(404, "post_not_found"))
        with pytest.raises(Status200Error) as raised:
            client.get_post(POST_ID)
        assert (raised.value.status, raised.value.code) == (404, "post_not_found")


class TestCancel:
    def test_cancel_and_cancel_again(self, make_client, spec) -> None:
        example = spec["components"]["schemas"]["CancelResult"]["example"]
        again = {"data": {**example["data"], "already_cancelled": True}}
        client, script = make_client(json_reply(200, example), json_reply(200, again))
        assert client.cancel(SCHEDULED_ID) == example["data"]
        assert client.cancel(SCHEDULED_ID)["already_cancelled"] is True
        request = script.requests[0]
        assert (request.method, request.url.path) == ("DELETE", f"/api/v2/posts/{SCHEDULED_ID}")
        assert "idempotency-key" not in request.headers

    def test_cancel_unconfirmed_is_sent_again(self, make_client, sleeps, spec) -> None:
        example = spec["components"]["schemas"]["CancelResult"]["example"]
        client, _ = make_client(
            error_reply(
                504, "cancel_unconfirmed", {"retry_after_seconds": 5}, {"Retry-After": "5"}
            ),
            json_reply(200, example),
        )
        assert client.cancel(SCHEDULED_ID)["status"] == "cancelled"
        assert sleeps == [5]

    def test_not_cancellable(self, make_client) -> None:
        client, script = make_client(error_reply(409, "not_cancellable", {"status": "published"}))
        with pytest.raises(Status200Error) as raised:
            client.cancel(SCHEDULED_ID)
        assert raised.value.details["status"] == "published"
        assert len(script.requests) == 1


class TestMedia:
    def test_a_ready_import(self, make_client, spec) -> None:
        ready = spec["components"]["schemas"]["MediaImportReady"]["example"]
        client, script = make_client(json_reply(200, ready))
        assert client.import_media("https://example.com/photo.jpg") == ready
        request = script.requests[0]
        assert (request.method, request.url.path) == ("POST", "/api/v2/media")
        assert body_of(request) == {"url": "https://example.com/photo.jpg"}
        uuid.UUID(request.headers["idempotency-key"])

    def test_waits_until_ready(self, make_client, sleeps) -> None:
        started = {
            "success": True,
            "file_id": FILE_ID,
            "status": "processing",
            "message": "Import started",
            "size": 1,
            "type": "video/mp4",
        }

        def status(state: str) -> httpx.Response:
            return json_reply(
                200,
                {
                    "success": state == "ready",
                    "file_id": FILE_ID,
                    "status": state,
                    "size": 1,
                    "type": "video/mp4",
                    "public_url": None,
                    "error": None,
                },
            )

        client, script = make_client(
            json_reply(202, started), status("processing"), status("processing"), status("ready")
        )
        media = client.import_media("https://example.com/video.mp4")
        assert media["status"] == "ready"
        assert sleeps == [5, 5]
        reads = script.requests[1:]
        assert {(r.method, r.url.path, r.url.params["file_id"]) for r in reads} == {
            ("GET", "/api/v2/media", FILE_ID)
        }

    def test_a_failed_import_raises(self, make_client, sleeps) -> None:
        failed = {
            "success": False,
            "file_id": FILE_ID,
            "status": "failed",
            "size": None,
            "type": None,
            "public_url": None,
            "error": "The file could not be downloaded",
        }
        client, _ = make_client(json_reply(200, failed))
        with pytest.raises(Status200Error) as raised:
            client.wait_for_media(FILE_ID)
        assert (raised.value.reason, raised.value.code) == ("import_failed", "media_failed")
        assert "could not be downloaded" in str(raised.value)

    def test_an_accepted_import_keeps_its_file_id_when_its_status_cannot_be_read(
        self, make_client, sleeps
    ) -> None:
        started = {
            "success": True,
            "file_id": FILE_ID,
            "status": "processing",
            "message": "Import started",
            "size": 1,
            "type": "video/mp4",
        }
        client, _ = make_client(
            json_reply(202, started),
            error_reply(500, "server_error"),
            error_reply(500, "server_error"),
        )
        assert client.import_media("https://example.com/video.mp4") == started

    def test_posts_and_media_use_separate_keys(self, make_client) -> None:
        ready = {
            "success": True,
            "file_id": FILE_ID,
            "size": 1,
            "type": "image/jpeg",
            "status": "ready",
        }
        client, script = make_client(json_reply(200, ready), json_reply(200, {"data": {}}))
        client.import_media("https://example.com/photo.jpg")
        client.publish({**POST, "content": {"text": "Hi", "mediaID": [FILE_ID]}})
        media_key, post_key = (r.headers["idempotency-key"] for r in script.requests)
        assert media_key != post_key

    def test_a_refused_import_carries_the_sentence(self, make_client) -> None:
        message = "The URL does not return an image or a video."
        client, _ = make_client(json_reply(415, {"error": message}))
        with pytest.raises(Status200Error) as raised:
            client.import_media("https://example.com/page.html")
        assert (raised.value.status, raised.value.code) == (415, None)
        assert raised.value.message == message
