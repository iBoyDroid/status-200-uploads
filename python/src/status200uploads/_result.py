"""What a successful POST /posts returns: Result, and the status200 ids in it."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Status200Ids:
    """Our ids for a post or a scheduled post (the answer's "status200" object).

    Present on every answer that recorded a post in History or a scheduled post, never on a dry
    run. Use post_id rather than data.post_id, which is the network's own id on Facebook, LinkedIn
    and Skool. status_url is GET /posts/{id}: Status200.wait_for() reads it.
    """

    post_id: str | None
    scheduled_post_id: str | None
    status_url: str | None

    @classmethod
    def from_body(cls, body: Mapping[str, Any] | None) -> Status200Ids | None:
        ids = body.get("status200") if isinstance(body, Mapping) else None
        if not isinstance(ids, Mapping):
            return None

        def text(key: str) -> str | None:
            value = ids.get(key)
            return value if isinstance(value, str) and value else None

        return cls(
            post_id=text("post_id"),
            scheduled_post_id=text("scheduled_post_id"),
            status_url=text("status_url"),
        )


@dataclass
class Result:
    """The answer to Status200.publish(): a 200 (published, or a dry run's report) or a 202
    (scheduled, queued for the next UTC day, processing, or still publishing). A 202 is never a
    failure and is never sent again."""

    #: 200 or 202.
    status_code: int
    #: The JSON answer, as the API sent it.
    raw: dict[str, Any]
    #: Response headers, names in lower case.
    headers: Mapping[str, str]
    #: True when this is the stored first answer to the Idempotency-Key (Idempotent-Replayed).
    replayed: bool
    #: The Idempotency-Key the request carried (None when it was sent without one). Keep it: the
    #: same request with the same key within 24 hours gets this answer again, and never posts twice.
    idempotency_key: str | None
    #: How many requests were sent in all, the first included.
    tries: int
    #: With publish(wait=True): the post as GET /posts/{id} last read it (status, done, permalink).
    final: dict[str, Any] | None = None

    @property
    def data(self) -> Any:
        """The network's result (200), or the 202's data (processing, scheduled)."""
        return self.raw.get("data")

    @property
    def code(self) -> str | None:
        """A 202's case: scheduled, queued_for_next_day, still_publishing, schedule_unconfirmed;
        None on a 200, and on a 202 that is processing (data.status)."""
        code = self.raw.get("code")
        return code if isinstance(code, str) else None

    @property
    def message(self) -> str | None:
        message = self.raw.get("message")
        return message if isinstance(message, str) else None

    @property
    def status200(self) -> Status200Ids | None:
        return Status200Ids.from_body(self.raw)

    @property
    def warnings(self) -> list[dict[str, Any]]:
        """Fields that were not used, and other things to know. The post was still sent."""
        warnings = self.raw.get("warnings")
        return [w for w in warnings if isinstance(w, dict)] if isinstance(warnings, list) else []

    @property
    def accepted(self) -> bool:
        """A 202: accepted and not published yet (it goes out on its own)."""
        return self.status_code == 202

    @property
    def dry_run(self) -> bool:
        """A dry run's report (nothing was sent): see would_publish, outcome and reason in raw."""
        return self.raw.get("dry_run") is True
