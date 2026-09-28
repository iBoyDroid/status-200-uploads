"""The errors the client raises.

Status200Error: the API refused the request, or the client stopped sending it again (the retry
table's rule, max_tries or max_wait). OutcomeUnknown, a Status200Error: the client cannot tell
whether a post (or a media import) went through.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ._answer import Answer
from ._result import Status200Ids

#: Why the client stopped.
REASONS = {
    # The retry table says never (or the answer contradicts itself).
    "refused",
    # Waiting as the API asked would pass max_wait.
    "max_wait",
    # Sent as often as allowed (max_tries, or twice for a "nothing was sent" code).
    "tries_used",
    # The outcome may not be known, and without an Idempotency-Key it is not sent again.
    "no_key",
    # Sent once more with the same Idempotency-Key, and the outcome is still not known.
    "once_used",
    # A media import that failed (GET /media says status "failed").
    "import_failed",
}


class Status200Error(Exception):
    """A request the API refused, or one the client stopped sending again.

    Branch on ``code`` (the API's error code, such as ``rate_limited`` or ``account_not_found``),
    not on ``status`` alone; ``message`` is the API's sentence for a person. ``details`` is the
    error object as the API sent it, with the refusal's facts (``resets_at``, ``profiles``,
    ``upgrade_url``, ...). ``note`` says what the client did and why it stopped; ``str(error)``
    is the message, the note, the status and the code.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: str | None = None,
        details: Mapping[str, Any] | None = None,
        rule: str | None = None,
        reason: str = "refused",
        retry_after_seconds: int | None = None,
        idempotency_key: str | None = None,
        tries: int = 1,
        waited_seconds: float = 0,
        answer: Answer | None = None,
        note: str = "",
    ) -> None:
        super().__init__(message)
        #: The API's sentence, or the client's when the API sent none.
        self.message = message
        #: What the client did and why it stopped ("" when the API refused it outright).
        self.note = note
        #: The HTTP status; 0 when no answer arrived.
        self.status = status
        #: The API's error code (None for an answer that was not JSON or carried none).
        self.code = code
        #: The error object as the API sent it.
        self.details: dict[str, Any] = dict(details or {})
        #: The retry table's rule of the last answer.
        self.rule = rule
        #: Why the client stopped: see errors.REASONS.
        self.reason = reason
        #: The wait the last answer asked for (Retry-After, else retry_after_seconds).
        self.retry_after_seconds = retry_after_seconds
        #: The Idempotency-Key the request carried.
        self.idempotency_key = idempotency_key
        #: How many requests were sent in all, the first included.
        self.tries = tries
        #: How long the client waited in all before sending again (seconds).
        self.waited_seconds = waited_seconds
        #: The last answer's JSON body (None when it was not JSON).
        self.body: dict[str, Any] | None = answer.body if answer else None
        #: The last answer's headers, names in lower case.
        self.headers: dict[str, str] = dict(answer.headers) if answer else {}
        #: The start of a body that was not JSON, or why no answer arrived.
        self.text = answer.text if answer else ""
        #: Whether the last answer was a replay of the first answer to the Idempotency-Key.
        self.replayed = answer.replayed if answer else False

    @property
    def upgrade_url(self) -> str | None:
        """On a plan refusal (plan_required, monthly_limit_reached, daily_limit_reached)."""
        value = self.details.get("upgrade_url")
        return value if isinstance(value, str) else None

    @property
    def status200(self) -> Status200Ids | None:
        """Our ids when the failure still left a post in History (a network's refusal)."""
        return Status200Ids.from_body(self.body)

    def __str__(self) -> str:
        where = f"HTTP {self.status}" if self.status else "no answer"
        facts = f"{where}, code {self.code}" if self.code else where
        text = f"{self.message} {self.note}" if self.note else self.message
        return f"{text} [{facts}]"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(status={self.status!r}, code={self.code!r}, "
            f"reason={self.reason!r}, message={self.message!r})"
        )


class OutcomeUnknown(Status200Error):
    """The client cannot tell whether the post (or the media import) went through.

    Check your posts (Status200.list_posts(), or History in the dashboard) before sending it again.
    Sending it again with the same ``idempotency_key`` within 24 hours never posts twice: a post
    that went through is answered with its first answer.
    """
