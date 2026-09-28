"""Shared test helpers: the OpenAPI file, a scripted transport that answers in order and records
every request, and a stand-in for time.sleep that records the waits instead of sleeping."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import pytest
from ruamel.yaml import YAML

from status200uploads import Status200

REPO = Path(__file__).resolve().parents[2]
SPEC_PATH = REPO / "openapi" / "openapi.yaml"

# Not a real key: tests never reach the network (every request goes to a MockTransport).
TEST_KEY = "not-a-real-key-only-for-tests"


def load_spec() -> dict[str, Any]:
    yaml = YAML(typ="safe", pure=True)
    return json.loads(json.dumps(yaml.load(SPEC_PATH.read_text(encoding="utf-8"))))


@pytest.fixture(scope="session")
def spec() -> dict[str, Any]:
    return load_spec()


def response_examples(spec: dict[str, Any], name: str) -> dict[str, Any]:
    """The named examples of a response in components.responses (Published, Accepted ...)."""
    content = spec["components"]["responses"][name]["content"]["application/json"]
    return {key: example["value"] for key, example in content["examples"].items()}


Reply = httpx.Response | Exception | Callable[[httpx.Request], httpx.Response]


def json_reply(status: int, body: Any, headers: dict[str, str] | None = None) -> httpx.Response:
    return httpx.Response(status, json=body, headers=headers or {})


def error_reply(
    status: int,
    code: str,
    extra: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """An ErrorResponse, as /api/v2 posts and reads answer."""
    return json_reply(
        status, {"error": {"code": code, "message": f"{code} message", **(extra or {})}}, headers
    )


def page_reply(
    status: int, text: str = "<html><body>Gateway Timeout</body></html>"
) -> httpx.Response:
    """A gateway's page that is not JSON (Netlify's 504 after 30 seconds)."""
    return httpx.Response(status, text=text, headers={"content-type": "text/html"})


class Script:
    """A transport that gives the scripted replies in order and records the requests."""

    def __init__(self, *replies: Reply) -> None:
        self.replies: list[Reply] = list(replies)
        self.requests: list[httpx.Request] = []

    def add(self, *replies: Reply) -> Script:
        self.replies.extend(replies)
        return self

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        if not self.replies:
            raise AssertionError(f"no scripted reply for {request.method} {request.url}")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if callable(reply) and not isinstance(reply, httpx.Response):
            return reply(request)
        return reply

    @property
    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self)


class Sleeps(list):
    """The waits the client asked for, in seconds."""


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> Sleeps:
    waits = Sleeps()
    monkeypatch.setattr("status200uploads._client._sleep", waits.append)
    return waits


@pytest.fixture
def make_client(sleeps: Sleeps) -> Callable[..., tuple[Status200, Script]]:
    """A Status200 on a scripted transport: make_client(reply, reply, ..., **Status200 kwargs)."""
    made: list[Status200] = []

    def make(*replies: Reply, **kwargs: Any) -> tuple[Status200, Script]:
        script = Script(*replies)
        kwargs.setdefault("api_key", TEST_KEY)
        client = Status200(httpx_args={"transport": script.transport}, **kwargs)
        made.append(client)
        return client, script

    yield make
    for client in made:
        client.close()
