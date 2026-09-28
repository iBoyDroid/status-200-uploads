"""Against the real API, only when STATUS200_API_KEY is set (skipped otherwise, and in CI).

Reads and dry runs only: nothing here can post, schedule or import anything. The key goes from the
environment straight into the client (never into a variable of a test, so no failure output can
show it). A real post, sent twice under one Idempotency-Key to prove the replay, belongs to the
release's live proof, not to this file.

    STATUS200_API_KEY=... pytest python/tests/test_live.py
"""

from __future__ import annotations

import os
import uuid

import pytest

from status200uploads import Status200, Status200Error

pytestmark = pytest.mark.skipif(
    not os.environ.get("STATUS200_API_KEY"), reason="set STATUS200_API_KEY to run against the API"
)

TEXT_NETWORKS = ("linkedin", "x", "threads", "facebook")


@pytest.fixture(scope="module")
def s200():
    with Status200() as client:
        yield client


@pytest.fixture(scope="module")
def accounts(s200):
    return s200.list_accounts()


def test_accounts_have_the_documented_shape(accounts) -> None:
    for account in accounts:
        assert {"profile_id", "profile_name", "handle", "networks"} <= set(account)
        uuid.UUID(account["profile_id"])
        assert account["handle"].startswith("@")


def test_a_dry_run_sends_nothing_and_reports(s200, accounts) -> None:
    found = [
        (account, network["platform"])
        for account in accounts
        for network in account["networks"]
        if network["platform"] in TEXT_NETWORKS and network.get("health") == "ready"
    ]
    if not found:
        pytest.skip("no profile with LinkedIn, X, Threads or Facebook ready")
    account, platform = found[0]
    report = s200.validate(
        {
            "accountId": account["profile_id"],
            "platform": platform,
            "content": {"text": "status200uploads live test: a dry run, never sent"},
        }
    )
    assert report["dry_run"] is True
    assert report["outcome"] in ("publish", "queue", "refuse", "schedule")
    assert report["target"]["platform"] == platform


def test_list_posts_pages(s200) -> None:
    page = s200.list_posts(limit=1)
    assert {"data", "next_cursor", "next_url"} <= set(page)
    assert len(page["data"]) <= 1


def test_an_unknown_post_is_404_post_not_found(s200) -> None:
    with pytest.raises(Status200Error) as raised:
        s200.get_post(str(uuid.uuid4()))
    assert (raised.value.status, raised.value.code) == (404, "post_not_found")
    assert raised.value.rule == "never"
