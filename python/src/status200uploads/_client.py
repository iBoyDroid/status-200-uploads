"""Status200: the hand-written client over the generated one.

The generated client (status200uploads._generated) has no base URL, no timeout (it passes
timeout=None to httpx), no Idempotency-Key, no retries, and loses the status and headers of an
answer that is not JSON. This layer adds exactly that, with no dependency beyond the generated
client's own (httpx, attrs):

- the base URL https://status200uploads.com/api/v2 and a timeout (120 s, 10 s to connect);
- the API key from the argument or STATUS200_API_KEY, sent as Authorization: Bearer, never shown
  in a repr, a log or an error;
- a User-Agent status200uploads-python/<version>;
- an automatic Idempotency-Key on every POST: one key per post (and a separate one per media
  import), reused on every try with the byte-identical body;
- waits and resends only what the API's retry table allows (components.x-status200-retry,
  copied in _retry.py), within max_tries and max_wait;
- wait_for(): reads status200.status_url every 30 seconds, for up to 10 minutes; it never posts.
"""

from __future__ import annotations

import datetime as _dt
import json
import logging
import os
import re
import time
import uuid
from collections.abc import Callable, Iterator, Mapping, Sequence
from typing import Any, Self

import httpx

from ._answer import Answer, no_answer, read_answer
from ._generated.client import AuthenticatedClient
from ._result import Result, Status200Ids
from ._retry import DEFAULT_WAIT_SECONDS, UNAVAILABLE_CODES, UNAVAILABLE_RESENDS
from ._version import __version__
from .errors import OutcomeUnknown, Status200Error

logger = logging.getLogger("status200uploads")

#: The API (the OpenAPI file's server).
DEFAULT_BASE_URL = "https://status200uploads.com/api/v2"
#: The API answers within about 25 seconds; a media import within about 22.
DEFAULT_TIMEOUT = httpx.Timeout(120.0, connect=10.0)
#: Where the API key is read from when none is passed.
API_KEY_ENV = "STATUS200_API_KEY"
USER_AGENT = f"status200uploads-python/{__version__}"

#: Requests sent for one call at most, the first included.
DEFAULT_MAX_TRIES = 5
#: The most the client waits in all, when the API asks it to wait, before giving up (seconds).
DEFAULT_MAX_WAIT = 120.0
#: wait_for(): read the post every 30 seconds, for up to 10 minutes (the documented stop).
POLL_INTERVAL = 30.0
POLL_TIMEOUT = 600.0
#: wait_for_media(): media status reads are not throttled or counted.
MEDIA_POLL_INTERVAL = 5.0

#: Idempotency-Key: 1 to 255 printable ASCII characters (parameters.IdempotencyKey of the file).
KEY_MAX_LENGTH = 255
KEY_PATTERN = re.compile(r"^[\x20-\x7E]+$")
#: The characters JavaScript's String.prototype.trim() removes: the API trims the key with it.
_TRIM = " \t\n\x0b\x0c\r                 　﻿"

#: The requests this client sends (method, path on the base URL, query parameters it may add).
#: tests/test_contract.py holds each to an operation of the OpenAPI file's main address.
ENDPOINTS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "publish": ("POST", "/posts", ()),
    "list_posts": (
        "GET",
        "/posts",
        ("limit", "cursor", "status", "platform", "kind", "profile_id"),
    ),
    "get_post": ("GET", "/posts/{id}", ()),
    "cancel": ("DELETE", "/posts/{id}", ()),
    "list_accounts": ("GET", "/accounts", ()),
    "get_posting_options": (
        "GET",
        "/accounts/{profile_id}/options",
        ("platforms", "skool_group_slug"),
    ),
    "import_media": ("POST", "/media", ()),
    "get_media": ("GET", "/media", ("file_id",)),
}

# Waits go through this name, so tests can stand in for time.sleep.
_sleep: Callable[[float], None] = time.sleep


class _Client(AuthenticatedClient):
    """The generated AuthenticatedClient, with a repr that never shows the API key (attrs' own
    repr prints every field, the token and the Authorization header included)."""

    __slots__ = ()

    def __repr__(self) -> str:
        return f"AuthenticatedClient(base_url={self._base_url!r}, token='[hidden]')"


def _json_default(value: Any) -> Any:
    if isinstance(value, _dt.datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                f"The time {value.isoformat()} has no time zone, and the API refuses such a time "
                "(400 scheduled_for_invalid, reason no_time_zone). Give it one, for example "
                "datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc), or .astimezone() for local time."
            )
        return value.isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    raise TypeError(f"{type(value).__name__} cannot be sent as JSON")


def _encode(body: Mapping[str, Any]) -> bytes:
    """The request body, serialised once: every try sends these same bytes (the API answers 422
    idempotency_key_reused to a key sent again with a different body)."""
    return json.dumps(
        body, ensure_ascii=False, separators=(",", ":"), default=_json_default
    ).encode("utf-8")


def _as_dict(value: Any, what: str) -> dict[str, Any]:
    if hasattr(value, "to_dict") and callable(value.to_dict):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise TypeError(f"{what} must be a dict or a status200uploads.models object")
    return dict(value)


def _request_body(post: Any, *, scheduled_for: Any = None, dry_run: bool = False) -> dict[str, Any]:
    """{"post": {...}} (plus dryRun) from a post (a dict or models.Post) or a whole request
    (a dict with a "post" key, or models.PostRequest). The caller's objects are not changed."""
    given = _as_dict(post, "post")
    body: dict[str, Any] = dict(given) if "post" in given else {"post": given}
    body["post"] = _as_dict(body["post"], "post")
    if scheduled_for is not None:
        body["post"]["scheduledFor"] = scheduled_for
    if dry_run:
        body["dryRun"] = True
    return body


def _is_dry_run(body: Mapping[str, Any]) -> bool:
    post = body.get("post")
    places = [body] + ([post] if isinstance(post, Mapping) else [])
    return any(place.get(name) is True for place in places for name in ("dryRun", "dry_run"))


def _key(value: str | bool | None) -> str | None:
    """None: a new key (a UUID); False: no key; a string: that key, read exactly as the API reads
    it: whitespace around it trimmed, then one pair of surrounding double quotes removed, then
    1 to 255 printable ASCII characters. Result.idempotency_key is therefore the key the API uses."""
    if value is None or value is True:
        return str(uuid.uuid4())
    if value is False:
        return None
    if not isinstance(value, str):
        raise TypeError("idempotency_key must be a string, None (automatic) or False (none)")
    value = value.strip(_TRIM)
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if not value or len(value) > KEY_MAX_LENGTH or not KEY_PATTERN.fullmatch(value):
        raise ValueError(
            f"idempotency_key must be 1 to {KEY_MAX_LENGTH} printable ASCII characters "
            "(a UUID, for example)"
        )
    return value


def _asked_wait(answer: Answer) -> int:
    """The wait an answer asks for: Retry-After, else retry_after_seconds, else 5 seconds."""
    for seconds in (answer.retry_after_header, answer.retry_after_seconds):
        if seconds is not None:
            return max(1, seconds)
    return DEFAULT_WAIT_SECONDS


def _uuid(value: Any, what: str) -> str:
    try:
        return str(uuid.UUID(str(value)))
    except (ValueError, TypeError, AttributeError):
        raise ValueError(f"{what} must be a UUID, not {value!r}") from None


def _post_id(target: Any) -> str:
    """The id to read from a Result, Status200Ids, a status_url or an id."""
    if isinstance(target, Result):
        if target.dry_run:
            raise ValueError("A dry run records nothing, so there is nothing to wait for")
        ids = target.status200
        if ids is None:
            raise ValueError(
                "This answer names no post to follow (no status200): check list_posts() instead"
            )
        target = ids
    if isinstance(target, Status200Ids):
        target = target.post_id or target.scheduled_post_id or target.status_url
    if isinstance(target, str) and "/" in target:
        # A status_url: https://status200uploads.com/api/v2/posts/<id>. Only its id is used; the
        # request goes to this client's base URL, so the key is never sent anywhere else.
        target = httpx.URL(target.strip()).path.rstrip("/").rsplit("/", 1)[-1]
    return _uuid(target, "The post id")


class Status200:
    """A client of the Status 200 Uploads API.

    >>> from status200uploads import Status200
    >>> s200 = Status200()  # the key from STATUS200_API_KEY
    >>> result = s200.publish({"accountId": "@myprofile", "platform": "linkedin",
    ...                        "content": {"text": "Hello from Python"}})
    >>> s200.wait_for(result)["permalink"]

    Every call returns the API's JSON (dicts and lists, as documented at
    https://status200uploads.com/docs/api) or raises Status200Error. The generated, typed layer is
    there too: status200uploads.models for request and answer objects, status200uploads.api for
    the raw operations (pass them ``client=s200.client``).
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: httpx.Timeout | float | None = DEFAULT_TIMEOUT,
        max_tries: int = DEFAULT_MAX_TRIES,
        max_wait: float = DEFAULT_MAX_WAIT,
        httpx_args: Mapping[str, Any] | None = None,
    ) -> None:
        """
        Args:
            api_key: An API key from your dashboard's API page (rl_...). Default: the
                STATUS200_API_KEY environment variable.
            base_url: The API's address.
            timeout: httpx's timeout for one request (default 120 s, 10 s to connect).
            max_tries: Requests sent for one call at most, the first included.
            max_wait: The most the client waits in all when the API asks it to wait before sending
                again (Retry-After), in seconds. 0 never waits: the error says how long to wait.
            httpx_args: More arguments for httpx.Client (a proxy, a transport, ...).
        """
        key = api_key if api_key is not None else os.environ.get(API_KEY_ENV, "")
        if not isinstance(key, str):
            raise TypeError("api_key must be a string")
        key = key.strip()
        if not key:
            raise ValueError(
                f"No API key: pass api_key=... or set the {API_KEY_ENV} environment variable. "
                "Create a key on the API page of your Status 200 Uploads dashboard."
            )
        if max_tries < 1:
            raise ValueError("max_tries must be 1 or more")
        if max_wait < 0:
            raise ValueError("max_wait must be 0 or more")
        if isinstance(timeout, bool):
            raise TypeError("timeout must be an httpx.Timeout, a number of seconds, or None")
        http_timeout = (
            httpx.Timeout(float(timeout)) if isinstance(timeout, int | float) else timeout
        )
        self.base_url = base_url.rstrip("/")
        self.max_tries = max_tries
        self.max_wait = float(max_wait)
        self._client = _Client(
            base_url=self.base_url,
            token=key,
            timeout=http_timeout,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            httpx_args=dict(httpx_args or {}),
        )
        self._http = self._client.get_httpx_client()

    def __repr__(self) -> str:
        return f"Status200(base_url={self.base_url!r})"

    # -- lifecycle ---------------------------------------------------------------------------

    @property
    def client(self) -> AuthenticatedClient:
        """The generated client, sharing this one's connection, key, timeout and User-Agent: pass
        it to the operations in status200uploads.api. They send each request once, as it is."""
        return self._client

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- sending -----------------------------------------------------------------------------

    def _send(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str] | None = None,
        content: bytes | None = None,
        key: str | None = None,
    ) -> Answer:
        headers = {}
        if content is not None:
            headers["Content-Type"] = "application/json"
        if key is not None:
            headers["Idempotency-Key"] = key
        try:
            response = self._http.request(
                method, path, params=params, content=content, headers=headers
            )
        except httpx.UnsupportedProtocol:
            # A base_url that is not http(s): nothing was sent, and nothing will be.
            raise
        except httpx.TransportError as exc:
            return no_answer(f"{type(exc).__name__}: {exc}")
        return read_answer(response)

    def _settle(
        self,
        send: Callable[[], Answer],
        *,
        what: str,
        key: str | None,
        repeatable: bool,
        max_tries: int | None = None,
        max_wait: float | None = None,
    ) -> tuple[Answer, int]:
        """Sends a request and follows the retry table to a final answer: waits and sends the
        identical request again only where the table allows it, within max_tries and max_wait.
        Returns the success (a 2xx with JSON) and how many requests were sent; raises otherwise."""
        max_tries = self.max_tries if max_tries is None else max_tries
        max_wait = self.max_wait if max_wait is None else float(max_wait)
        answer = send()
        tries = 1
        waited = 0.0
        unavailable_resends = 0
        resent_once = False

        def stop(reason: str) -> Status200Error:
            rule = answer.rule
            # A POST that may have gone through: no clear answer, the first request with this key
            # never answered, or it is still running and the client stopped waiting for it.
            unknown = not repeatable and (
                rule == "resend_once_with_key"
                or answer.code in ("idempotency_outcome_unknown", "idempotency_in_progress")
            )
            asked = _asked_wait(answer) if rule == "wait_and_resend" else None
            cls = OutcomeUnknown if unknown else Status200Error
            return cls(
                _said(answer, what),
                note=_note(
                    answer,
                    what=what,
                    reason=reason,
                    asked=asked,
                    key=key,
                    tries=tries,
                    max_wait=max_wait,
                    unknown=unknown,
                ),
                status=answer.status,
                code=answer.code,
                details=answer.error,
                rule=rule,
                reason=reason,
                retry_after_seconds=asked
                if asked is not None
                else (
                    answer.retry_after_header
                    if answer.retry_after_header is not None
                    else answer.retry_after_seconds
                ),
                idempotency_key=key,
                tries=tries,
                waited_seconds=waited,
                answer=answer,
            )

        while True:
            if answer.ok:
                return answer, tries
            rule = answer.rule
            if rule == "wait_and_resend":
                wait = _asked_wait(answer)
                unavailable = answer.code in UNAVAILABLE_CODES
                if unavailable and unavailable_resends >= UNAVAILABLE_RESENDS:
                    raise stop("tries_used")
                if tries >= max_tries:
                    raise stop("tries_used")
                if waited + wait > max_wait:
                    raise stop("max_wait")
                if unavailable:
                    unavailable_resends += 1
                logger.info(
                    "%s: %s (HTTP %s); sending it again in %s s",
                    what,
                    answer.code,
                    answer.status,
                    wait,
                )
                _sleep(wait)
                waited += wait
                answer = send()
                tries += 1
                continue
            if rule == "resend_once_with_key":
                if key is None and not repeatable:
                    raise stop("no_key")
                if resent_once:
                    raise stop("once_used")
                if tries >= max_tries:
                    raise stop("tries_used")
                header = answer.retry_after_header
                wait = max(1, header) if header is not None else DEFAULT_WAIT_SECONDS
                logger.info(
                    "%s: %s (HTTP %s); sending it once more in %s s",
                    what,
                    answer.code or ("no answer" if answer.status == 0 else "not JSON"),
                    answer.status,
                    wait,
                )
                resent_once = True
                _sleep(wait)
                waited += wait
                answer = send()
                tries += 1
                continue
            # never, or "accepted" on an answer that is not a 2xx (it contradicts itself).
            raise stop("refused")

    # -- posts -------------------------------------------------------------------------------

    def publish(
        self,
        post: Any,
        *,
        scheduled_for: str | float | _dt.datetime | None = None,
        dry_run: bool = False,
        idempotency_key: str | bool | None = None,
        wait: bool = False,
        max_tries: int | None = None,
        max_wait: float | None = None,
    ) -> Result:
        """Publishes one post to one network now, or schedules it (POST /posts).

        Args:
            post: The post: a dict such as {"accountId": "@myprofile", "platform": "x",
                "content": {"text": "..."}} or a models.Post (a whole request, {"post": {...}} or
                models.PostRequest, works too). The fields are the API's (post.content.mediaID,
                post.tiktok.privacyLevel, post.pinterest.boardId ...).
            scheduled_for: When to publish: an ISO 8601 time with a time zone, a Unix time, or a
                datetime that has a time zone. More than 60 seconds ahead (up to 365 days) the post
                is scheduled: a 202 with code "scheduled".
            dry_run: Run every check a publish makes and send nothing (a 200 with dry_run true).
            idempotency_key: None (default): a new key for this post, reused on every try.
                A string: your own key (1 to 255 printable ASCII characters), for example your
                record's id and the network: the same key and body within 24 hours gets the
                first answer again and never posts twice. False: no key (an answer whose outcome is
                not known is then never sent again).
            wait: After a post that went to History (status200.post_id), wait for its result
                with wait_for() and put it in Result.final.
            max_tries, max_wait: Override the client's limits for this call.

        Returns:
            Result: a 200 (published, or a dry run's report) or a 202 (scheduled, queued for the
            next UTC day, processing, still publishing). Never sent again.

        Raises:
            Status200Error: the API refused it (code and message say why), or a wait it asked for
                passes max_wait.
            OutcomeUnknown: no clear answer, and it may have gone through: check list_posts()
                before sending it again.
        """
        body = _request_body(post, scheduled_for=scheduled_for, dry_run=dry_run)
        content = _encode(body)
        key = _key(idempotency_key)
        is_dry = _is_dry_run(body)
        answer, tries = self._settle(
            lambda: self._send("POST", "/posts", content=content, key=key),
            what="POST /posts",
            key=key,
            repeatable=is_dry,
            max_tries=max_tries,
            max_wait=max_wait,
        )
        result = Result(
            status_code=answer.status,
            raw=answer.body or {},
            headers=answer.headers,
            replayed=answer.replayed,
            idempotency_key=key,
            tries=tries,
        )
        ids = result.status200
        if wait and not result.dry_run and ids is not None and ids.post_id:
            try:
                result.final = self.wait_for(ids)
            except Status200Error as error:
                # The post was accepted: a read that fails must not look like a failed post (it
                # would invite sending it again). result.final stays None.
                logger.warning("The post was accepted, but reading its result failed: %s", error)
        return result

    def validate(
        self, post: Any, *, scheduled_for: str | float | _dt.datetime | None = None
    ) -> dict[str, Any]:
        """Checks a post without sending it (a dry run): the report says outcome (publish,
        schedule, queue or refuse), would_publish, reason and every check. Nothing is posted."""
        return self.publish(post, scheduled_for=scheduled_for, dry_run=True).raw

    def wait_for(
        self,
        target: Result | Status200Ids | str,
        *,
        interval: float = POLL_INTERVAL,
        timeout: float = POLL_TIMEOUT,
    ) -> dict[str, Any]:
        """Reads a post (GET /posts/{id}) every ``interval`` seconds until it is done, for up to
        ``timeout`` seconds (every 30 seconds for 10 minutes by default). Never sends the post
        again.

        Args:
            target: A Result of publish(), its status200, its status_url, or a post id.

        Returns:
            The post as last read: status (success, failed, processing, timeout ...), done,
            permalink, error_message. When timeout passes first it is the last state, not an error:
            a post still "processing" finishes by itself, and one in "timeout" must not be sent
            again.
        """
        post_id = _post_id(target)
        if interval <= 0:
            raise ValueError("interval must be more than 0")
        reads = max(1, int(timeout // interval))
        post: dict[str, Any] = {}
        for read in range(reads):
            post = self.get_post(post_id)
            if post.get("done") is True:
                break
            if read < reads - 1:
                _sleep(interval)
        return post

    def get_post(self, post_id: str | Status200Ids | Result) -> dict[str, Any]:
        """One post or scheduled post (GET /posts/{id}): its data. A status_url works too."""
        post_id = _post_id(post_id)
        return self._read(f"/posts/{post_id}", what="GET /posts/{id}").get("data") or {}

    def list_posts(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        status: str | Sequence[str] | None = None,
        platform: str | None = None,
        kind: str | None = None,
        profile_id: str | None = None,
    ) -> dict[str, Any]:
        """One page of your posts and waiting posts, newest first (GET /posts): {"data": [...],
        "next_cursor": ..., "next_url": ...}. iter_posts() follows the pages."""
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(int(limit))
        if cursor is not None:
            params["cursor"] = cursor
        if status is not None:
            params["status"] = status if isinstance(status, str) else ",".join(status)
        if platform is not None:
            params["platform"] = platform
        if kind is not None:
            params["kind"] = kind
        if profile_id is not None:
            params["profile_id"] = _uuid(profile_id, "profile_id")
        return self._read("/posts", what="GET /posts", params=params)

    def iter_posts(self, *, page_size: int = 100, **filters: Any) -> Iterator[dict[str, Any]]:
        """Every post and waiting post that matches the filters (those of list_posts), page after
        page. Each page is one of the 60 reads a minute your account has."""
        cursor = None
        seen: set[str] = set()
        while True:
            page = self.list_posts(limit=page_size, cursor=cursor, **filters)
            yield from page.get("data") or []
            cursor = page.get("next_cursor")
            if not cursor or cursor in seen:
                return
            seen.add(cursor)

    def cancel(self, scheduled_post_id: str | Status200Ids | Result) -> dict[str, Any]:
        """Cancels a post that has not gone out (DELETE /posts/{id}): its data. Cancelling twice
        is safe: the second answer says already_cancelled."""
        post_id = _post_id(scheduled_post_id)
        answer, _ = self._settle(
            lambda: self._send("DELETE", f"/posts/{post_id}"),
            what="DELETE /posts/{id}",
            key=None,
            repeatable=True,
        )
        return (answer.body or {}).get("data") or {}

    # -- accounts ----------------------------------------------------------------------------

    def list_accounts(self) -> list[dict[str, Any]]:
        """Your profiles, each with its connected networks and whether each can post now
        (GET /accounts). A profile's handle ("@name") or profile_id is a post's accountId."""
        return self._read("/accounts", what="GET /accounts").get("data") or []

    def get_posting_options(
        self,
        profile_id: str,
        *,
        platforms: str | Sequence[str] | None = None,
        skool_group_slug: str | None = None,
    ) -> dict[str, Any]:
        """What a profile may do on each network (GET /accounts/{profile_id}/options): the TikTok
        privacy levels it accepts, Pinterest boards, Skool groups, the Instagram publishing
        limit... Limited to 10 a minute per account."""
        profile_id = _uuid(profile_id, "profile_id")
        params: dict[str, str] = {}
        if platforms is not None:
            params["platforms"] = platforms if isinstance(platforms, str) else ",".join(platforms)
        if skool_group_slug is not None:
            params["skool_group_slug"] = skool_group_slug
        return (
            self._read(
                f"/accounts/{profile_id}/options",
                what="GET /accounts/{profile_id}/options",
                params=params,
            ).get("data")
            or {}
        )

    # -- media -------------------------------------------------------------------------------

    def import_media(
        self,
        url: str,
        *,
        wait: bool = True,
        idempotency_key: str | bool | None = None,
        interval: float = MEDIA_POLL_INTERVAL,
        timeout: float = POLL_TIMEOUT,
    ) -> dict[str, Any]:
        """Imports an image or a video from a public URL (POST /media), then, with wait=True,
        follows the import until it is ready. Send its file_id in post.content.mediaID.

        Returns:
            The media: file_id, status ("ready", or "processing" when timeout passed first:
            publish() then waits for it), size, type.

        Raises:
            Status200Error: the import was refused (message says why) or failed
                (reason "import_failed").
        """
        content = _encode({"url": url})
        key = _key(idempotency_key)
        answer, _ = self._settle(
            lambda: self._send("POST", "/media", content=content, key=key),
            what="POST /media",
            key=key,
            repeatable=False,
        )
        media = answer.body or {}
        if wait and media.get("status") == "processing" and media.get("file_id"):
            try:
                return self.wait_for_media(media["file_id"], interval=interval, timeout=timeout)
            except Status200Error as error:
                if error.reason == "import_failed":
                    raise
                # The import was accepted: return it as it stands (publish() waits for a file
                # that is still importing) rather than lose its file_id.
                logger.warning("The import was accepted, but reading its status failed: %s", error)
        return media

    def get_media(self, file_id: str) -> dict[str, Any]:
        """An import's status (GET /media?file_id=): status processing, ready or failed (with the
        reason in error), size, type, progress."""
        file_id = _uuid(file_id, "file_id")
        return self._read("/media", what="GET /media", params={"file_id": file_id})

    def wait_for_media(
        self,
        file_id: str,
        *,
        interval: float = MEDIA_POLL_INTERVAL,
        timeout: float = POLL_TIMEOUT,
    ) -> dict[str, Any]:
        """Reads an import every ``interval`` seconds until it is ready, for up to ``timeout``
        seconds. Returns the last status (still "processing" when timeout passed first); raises
        Status200Error (reason "import_failed") when the import failed."""
        if interval <= 0:
            raise ValueError("interval must be more than 0")
        reads = max(1, int(timeout // interval))
        media: dict[str, Any] = {}
        for read in range(reads):
            media = self.get_media(file_id)
            status = media.get("status")
            if status == "failed":
                reason = media.get("error") or "no reason given"
                raise Status200Error(
                    f"The import of {file_id} failed: {reason}",
                    status=200,
                    code="media_failed",
                    details=media,
                    reason="import_failed",
                )
            if status == "ready":
                break
            if read < reads - 1:
                _sleep(interval)
        return media

    # -- reads -------------------------------------------------------------------------------

    def _read(
        self, path: str, *, what: str, params: Mapping[str, str] | None = None
    ) -> dict[str, Any]:
        answer, _ = self._settle(
            lambda: self._send("GET", path, params=params or None),
            what=what,
            key=None,
            repeatable=True,
        )
        return answer.body or {}


def _said(answer: Answer, what: str) -> str:
    """The error's message: the API's sentence, or the client's when the API sent none."""
    if answer.message:
        return answer.message.strip()
    if answer.status == 0:
        return f"{what} got no answer ({answer.text or 'the connection closed'})."
    if not answer.json:
        return f"{what} got an answer that is not JSON (HTTP {answer.status}), such as a gateway's page."
    return f"{what} was answered HTTP {answer.status}."


def _note(
    answer: Answer,
    *,
    what: str,
    reason: str,
    asked: int | None,
    key: str | None,
    tries: int,
    max_wait: float,
    unknown: bool,
) -> str:
    """What the client did and why it stopped, and what to do when the outcome is not known."""
    parts = []
    if reason == "max_wait":
        parts.append(
            f"The API asked to wait {asked} s before sending it again, which passes "
            f"max_wait ({max_wait:g} s)."
        )
    elif reason == "tries_used":
        parts.append(f"Sent {tries} times in all.")
    elif reason == "no_key":
        parts.append("It was sent without an Idempotency-Key, so it is not sent again.")
    elif reason == "once_used":
        again = " with the same Idempotency-Key" if key else ""
        parts.append(f"Sent once more{again}, and the outcome is still not known.")
    if unknown and what.startswith("POST /media"):
        parts.append(
            "The import may have started: send it again with the same idempotency_key within 24 "
            "hours to get its file_id, or import the file again."
        )
    elif unknown:
        check = "It may have gone through: check your posts (list_posts() or History)"
        if answer.code == "idempotency_outcome_unknown":
            # The same key keeps getting this answer: only a new key sends it again.
            parts.append(
                f"{check}, and send it with a new idempotency_key only if it is not there."
            )
        elif key:
            parts.append(
                f"{check}, or send it again with the same idempotency_key within 24 hours, "
                "which never posts twice."
            )
        else:
            parts.append(f"{check} before sending it again.")
    return " ".join(parts)
