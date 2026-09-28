"""One answer of the API, read the same way whatever its shape.

    /api/v2 posts and reads  {"error": {"code", "message", ...}}  (ErrorResponse)
    /api/v2/media            {"error": "sentence", "code"?, "retry_after_seconds"?}  (MediaError);
                             its 429 import_budget_exhausted carries an object in "error" instead
    a 2xx                    the body itself (a 202 names its case in "code")
    not JSON                 a gateway's page (Netlify's HTML 504 after 30 seconds), or no answer
                             at all: the connection broke or timed out (status 0)

The generated client's *_detailed functions cannot be used for this: they call response.json() on
every status (a gateway's HTML page raises json.JSONDecodeError) and HTTPStatus(status) (a status
outside the standard list raises ValueError), and the status and headers the retry table needs are
lost with the exception.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import httpx

from ._retry import Rule, retry_rule

#: How much of a body that is not JSON is kept (for the error message).
TEXT_KEPT = 500


def _seconds(value: Any) -> int | None:
    """A wait in whole seconds (rounded up), from a number or a numeric string; else None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        try:
            value = float(value.strip())
        except ValueError:
            return None
    if isinstance(value, int | float) and math.isfinite(value) and value >= 0:
        return math.ceil(value)
    return None


def _string(value: Any) -> str | None:
    return value if isinstance(value, str) else None


@dataclass(frozen=True)
class Answer:
    """One HTTP answer (or the lack of one), as the retry table reads it."""

    #: The HTTP status; 0 when no answer arrived.
    status: int
    #: Response headers, names in lower case.
    headers: Mapping[str, str] = field(default_factory=dict)
    #: The JSON body when it is a JSON object; None otherwise.
    body: dict[str, Any] | None = None
    #: The start of a body that was not JSON, or why no answer arrived.
    text: str = ""
    #: error.code, the media shape's code, or a 2xx's code.
    code: str | None = None
    #: error.message, the media shape's error sentence, or a 2xx's message.
    message: str | None = None
    #: The Retry-After header, in seconds.
    retry_after_header: int | None = None
    #: error.retry_after_seconds, or retry_after_seconds next to a media error.
    retry_after_seconds: int | None = None
    #: Idempotent-Replayed: true (the stored first answer to this Idempotency-Key).
    replayed: bool = False

    @property
    def json(self) -> bool:
        return self.body is not None

    @property
    def ok(self) -> bool:
        """A 2xx with a JSON body: a success, never sent again."""
        return 200 <= self.status < 300 and self.body is not None

    @property
    def rule(self) -> Rule:
        return retry_rule(self.status, self.code, json=self.json)

    @property
    def error(self) -> dict[str, Any]:
        """The error object as the API sent it ({} when the answer has none)."""
        if self.body is None:
            return {}
        error = self.body.get("error")
        if isinstance(error, dict):
            return error
        if isinstance(error, str):
            # The media shape: the sentence in "error", its facts next to it.
            return {key: value for key, value in self.body.items() if key != "error"} | {
                "message": error
            }
        return {}


def _parse_body(content: bytes) -> dict[str, Any] | None:
    text = content.lstrip()
    if not text.startswith(b"{"):
        return None
    try:
        parsed = json.loads(text)
    except ValueError:
        # A page that happens to start with a brace: read as text.
        return None
    return parsed if isinstance(parsed, dict) else None


def read_answer(response: httpx.Response) -> Answer:
    """Reads one HTTP response."""
    headers = {name.lower(): value for name, value in response.headers.items()}
    body = _parse_body(response.content)
    status = response.status_code
    replayed = headers.get("idempotent-replayed", "").strip().lower() == "true"
    retry_after_header = _seconds(headers.get("retry-after"))
    if body is None:
        text = response.content[:TEXT_KEPT].decode("utf-8", errors="replace")
        return Answer(
            status=status,
            headers=headers,
            replayed=replayed,
            retry_after_header=retry_after_header,
            text=text,
        )

    error = body.get("error")
    if isinstance(error, dict):
        # ErrorResponse, and the media 429 import_budget_exhausted.
        code = _string(error.get("code")) or _string(body.get("code"))
        message = _string(error.get("message"))
        wait = _seconds(error.get("retry_after_seconds"))
        if wait is None:
            wait = _seconds(body.get("retry_after_seconds"))
    elif isinstance(error, str):
        # MediaError: the sentence in "error", the code (when any) next to it.
        code = _string(body.get("code"))
        message = error
        wait = _seconds(body.get("retry_after_seconds"))
    else:
        # A 2xx: a 202 names its case in "code" (scheduled, queued_for_next_day ...).
        code = _string(body.get("code"))
        message = _string(body.get("message"))
        wait = None
    return Answer(
        status=status,
        headers=headers,
        replayed=replayed,
        retry_after_header=retry_after_header,
        body=body,
        code=code,
        message=message,
        retry_after_seconds=wait,
    )


def no_answer(reason: str) -> Answer:
    """The Answer of a request that got none: the connection broke, or it timed out."""
    return Answer(status=0, text=reason[:TEXT_KEPT])
