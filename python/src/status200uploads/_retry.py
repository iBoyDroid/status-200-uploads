"""What the client may do with an answer: the API's retry table.

RETRY_TABLE is a copy of components.x-status200-retry of openapi/openapi.yaml (the file the service
publishes at https://status200uploads.com/openapi.yaml). tests/test_contract.py holds the two equal,
so a change of the API's table fails this package's tests until the client follows it. The n8n node
in this repository is tested against the same table.

The rules:
    wait_and_resend       nothing was sent, or the first answer comes back: wait (Retry-After, else
                          retry_after_seconds, else 5 seconds), then send the IDENTICAL request again:
                          the same body, byte for byte, and the same Idempotency-Key;
    resend_once_with_key  the outcome may not be known: send it once more, and only when it carried
                          an Idempotency-Key (a read, a cancel or a dry run may always be sent again);
    never                 the same request cannot succeed now;
    not_a_failure         accepted: it goes out on its own. Never sent again.

REST refusals carry code and message (and upgrade_url on a plan refusal). They carry no next_step
and no retry field: this table is how a client decides.
"""

from __future__ import annotations

from typing import Final, Literal

Rule = Literal["wait_and_resend", "resend_once_with_key", "never", "not_a_failure"]

RETRY_TABLE: Final[dict] = {
    "version": 1,
    "by_code": {
        "media_processing": "wait_and_resend",
        "idempotency_in_progress": "wait_and_resend",
        "rate_limited": "wait_and_resend",
        "caller_check_unavailable": "wait_and_resend",
        "schedule_check_unavailable": "wait_and_resend",
        "idempotency_unavailable": "wait_and_resend",
        "dry_run_unavailable": "wait_and_resend",
        "upstream_unavailable": "wait_and_resend",
        "cancel_unconfirmed": "wait_and_resend",
        "skool_unavailable": "wait_and_resend",
        "x_unavailable": "wait_and_resend",
        "platform_error": "resend_once_with_key",
        "server_error": "resend_once_with_key",
        "upload_worker_failed": "resend_once_with_key",
        "no_publish_id": "resend_once_with_key",
        "idempotency_outcome_unknown": "never",
        "idempotency_key_reused": "never",
        "monthly_limit_reached": "never",
        "daily_limit_reached": "never",
        "daily_attempts_exceeded": "never",
        "x_limit_reached": "never",
        "x_link_limit_reached": "never",
        "import_budget_exhausted": "never",
        "scheduled": "not_a_failure",
        "queued_for_next_day": "not_a_failure",
        "still_publishing": "not_a_failure",
        "schedule_unconfirmed": "not_a_failure",
    },
    "by_status": {
        "2xx": "not_a_failure",
        "4xx": "never",
        "5xx": "resend_once_with_key",
        "not_json": "resend_once_with_key",
    },
}

#: Codes that say "nothing was sent, a check could not run just now": sent again at most
#: UNAVAILABLE_RESENDS times, however short the wait.
UNAVAILABLE_CODES: Final = frozenset(
    {
        "caller_check_unavailable",
        "schedule_check_unavailable",
        "idempotency_unavailable",
        "dry_run_unavailable",
        "upstream_unavailable",
        "cancel_unconfirmed",
        "skool_unavailable",
        "x_unavailable",
    }
)
UNAVAILABLE_RESENDS: Final = 2

#: The wait (seconds) when an answer that asks for one names none.
DEFAULT_WAIT_SECONDS: Final = 5


def retry_rule(status: int, code: str | None = None, *, json: bool = True) -> Rule:
    """The rule of one answer: by its code first, else by its status class; an answer that is not
    JSON (a gateway's page, or no answer at all) is 'not_json'. The same order as the OpenAPI file's
    reader in the service's repository and the n8n node."""
    if not json:
        return RETRY_TABLE["by_status"]["not_json"]
    if isinstance(code, str) and code in RETRY_TABLE["by_code"]:
        return RETRY_TABLE["by_code"][code]
    return RETRY_TABLE["by_status"].get(f"{str(status)[:1]}xx", "never")
