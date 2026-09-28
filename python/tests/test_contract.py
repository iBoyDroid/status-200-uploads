"""The package against the OpenAPI file (../openapi/openapi.yaml, a copy of
https://status200uploads.com/openapi.yaml): its retry table is the file's, every request it sends
exists on the main address, the fields it writes and reads are the file's, and the generated code
covers exactly the main address's operations."""

from __future__ import annotations

import importlib
import pkgutil
import re

import httpx
import pytest
from conftest import response_examples

import status200uploads
from status200uploads import DEFAULT_BASE_URL, RETRY_TABLE, retry_rule
from status200uploads import _generated as generated
from status200uploads import api as api_shim
from status200uploads import models as models_shim
from status200uploads._client import (
    ENDPOINTS,
    KEY_MAX_LENGTH,
    KEY_PATTERN,
    POLL_INTERVAL,
    POLL_TIMEOUT,
)
from status200uploads._generated.api.posts import create_post
from status200uploads._generated.client import AuthenticatedClient
from status200uploads._retry import DEFAULT_WAIT_SECONDS, UNAVAILABLE_CODES

METHODS = ("get", "put", "post", "delete", "patch")


def v2_operations(spec: dict) -> dict[tuple[str, str], dict]:
    """The main address's operations: paths without a server of their own."""
    out = {}
    for path, item in spec["paths"].items():
        if "servers" in item:
            continue
        for method in METHODS:
            if method in item:
                out[(method.upper(), path)] = {"op": item[method], "item": item}
    return out


def deref(spec: dict, value: dict) -> dict:
    ref = value.get("$ref") if isinstance(value, dict) else None
    if not ref:
        return value
    at = spec
    for part in ref[2:].split("/"):
        at = at[part]
    return at


def schema(spec: dict, name: str) -> dict:
    return spec["components"]["schemas"][name]


def snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class TestRetryTable:
    def test_is_the_files_table(self, spec) -> None:
        table = spec["components"]["x-status200-retry"]
        assert RETRY_TABLE["version"] == table["version"]
        assert RETRY_TABLE["by_code"] == table["by_code"]
        assert RETRY_TABLE["by_status"] == table["by_status"]

    def test_knows_every_rule_and_no_other(self, spec) -> None:
        rules = set(spec["components"]["x-status200-retry"]["rules"])
        used = set(RETRY_TABLE["by_code"].values()) | set(RETRY_TABLE["by_status"].values())
        assert used <= rules
        assert rules == {"wait_and_resend", "resend_once_with_key", "never", "not_a_failure"}

    def test_reads_it_in_the_files_order(self, spec) -> None:
        # By code first, then by status class, then not_json (the file's reader does the same).
        for code, rule in spec["components"]["x-status200-retry"]["by_code"].items():
            assert retry_rule(418, code) == rule
        assert retry_rule(404, "no_such_code") == "never"
        assert retry_rule(503, "no_such_code") == "resend_once_with_key"
        assert retry_rule(200, None, json=False) == "resend_once_with_key"

    def test_the_default_wait_is_the_files(self, spec) -> None:
        assert (
            f"else {DEFAULT_WAIT_SECONDS} seconds"
            in (spec["components"]["x-status200-retry"]["rules"]["wait_and_resend"])
        )

    def test_the_nothing_was_sent_codes_are_the_files(self, spec) -> None:
        unavailable = deref(spec, spec["components"]["responses"]["PostsUnavailable"])
        documented = set(unavailable["x-error-codes"])
        cancel = v2_operations(spec)[("DELETE", "/posts/{id}")]["op"]
        documented |= set(cancel["responses"]["502"]["x-error-codes"])  # upstream_unavailable
        documented |= set(cancel["responses"]["504"]["x-error-codes"])  # cancel_unconfirmed
        assert UNAVAILABLE_CODES == documented

    def test_every_code_in_the_table_is_one_the_main_address_answers(self, spec) -> None:
        answered = set(schema(spec, "Accepted")["properties"]["code"]["x-known-values"])
        for found in v2_operations(spec).values():
            for response in found["op"]["responses"].values():
                answered |= set(deref(spec, response).get("x-error-codes", []))
        assert set(RETRY_TABLE["by_code"]) <= answered


class TestRequests:
    def test_the_base_url_is_the_files_server(self, spec) -> None:
        assert spec["servers"][0]["url"] == DEFAULT_BASE_URL

    @pytest.mark.parametrize("name", sorted(ENDPOINTS))
    def test_every_request_exists_on_the_main_address(self, spec, name) -> None:
        method, path, query = ENDPOINTS[name]
        found = v2_operations(spec).get((method, path))
        assert found is not None, f"{method} {path} is not an operation of the main address"
        params = [
            deref(spec, p)
            for p in [*found["item"].get("parameters", []), *found["op"].get("parameters", [])]
        ]
        declared = {p["name"] for p in params if p["in"] == "query"}
        assert set(query) <= declared
        if method == "POST":
            assert "Idempotency-Key" in {p["name"] for p in params if p["in"] == "header"}

    def test_every_operation_of_the_main_address_is_offered(self, spec) -> None:
        offered = {(method, path) for method, path, _ in ENDPOINTS.values()}
        assert offered == set(v2_operations(spec))

    def test_nothing_of_the_older_address_is_used(self, spec) -> None:
        older = {path for path, item in spec["paths"].items() if "servers" in item}
        assert older, "the file describes the older address"
        assert not older & {path for _, path, _ in ENDPOINTS.values()}
        assert all("functions/v1" not in server["url"] for server in spec["servers"])

    def test_the_idempotency_key_rules_are_the_files(self, spec) -> None:
        key_schema = spec["components"]["parameters"]["IdempotencyKey"]["schema"]
        assert KEY_PATTERN.pattern == key_schema["pattern"]
        assert KEY_MAX_LENGTH == key_schema["maxLength"]
        assert (
            KEY_MAX_LENGTH == spec["components"]["x-status200-limits"]["idempotency_key_max_length"]
        )
        assert key_schema["minLength"] == 1

    def test_the_ids_in_paths_are_uuids(self, spec) -> None:
        # The client checks ids as UUIDs before building a path.
        parameters = spec["components"]["parameters"]
        for name in ("PostId", "ProfileId", "FileId"):
            assert parameters[name]["schema"]["format"] == "uuid", name

    def test_the_body_fields_it_writes_are_the_files(self, spec) -> None:
        assert {"post", "dryRun"} <= set(schema(spec, "PostRequest")["properties"])
        assert {"accountId", "platform", "scheduledFor", "content"} <= set(
            schema(spec, "Post")["properties"]
        )
        assert set(schema(spec, "MediaImportRequest")["properties"]) == {"url"}

    def test_the_documented_wait_for_a_post(self, spec) -> None:
        description = v2_operations(spec)[("GET", "/posts/{id}")]["op"]["description"]
        assert f"every {POLL_INTERVAL:g} seconds" in description
        assert f"up to {POLL_TIMEOUT / 60:g} minutes" in description

    def test_the_list_page_limit_is_the_files(self, spec) -> None:
        limit = spec["components"]["parameters"]["Limit"]["schema"]
        # iter_posts() asks for full pages.
        assert limit["maximum"] == 100


class TestAnswers:
    def test_the_fields_it_reads_are_the_files(self, spec) -> None:
        ids = schema(spec, "Status200Ids")
        assert set(ids["required"]) == {"post_id", "scheduled_post_id", "status_url"}
        for name in ("PublishResult", "Accepted", "ErrorResponse"):
            assert "status200" in schema(spec, name)["properties"], name
        error = schema(spec, "ErrorObject")
        assert set(error["required"]) == {"code", "message"}
        assert {"retry_after_seconds", "upgrade_url"} <= set(error["properties"])
        media_error = schema(spec, "MediaError")["properties"]
        assert {"error", "code", "retry_after_seconds"} <= set(media_error)
        assert "done" in schema(spec, "PostItem")["required"]
        assert "next_cursor" in schema(spec, "PostList")["required"]
        assert set(schema(spec, "MediaStatus")["properties"]["status"]["x-known-values"]) == {
            "processing",
            "ready",
            "failed",
        }
        assert schema(spec, "DryRunReport")["properties"]["dry_run"]["const"] is True

    def test_the_headers_it_reads_are_the_files(self, spec) -> None:
        headers = spec["components"]["headers"]
        assert headers["RetryAfter"]["schema"]["type"] == "integer"
        assert headers["IdempotentReplayed"]["schema"]["enum"] == ["true"]

    def test_the_generated_models_read_every_answer_example(self, spec) -> None:
        client = AuthenticatedClient(base_url=DEFAULT_BASE_URL, token="not-a-key")
        for status, name in ((200, "Published"), (202, "Accepted")):
            for example_name, example in response_examples(spec, name).items():
                parsed = create_post._parse_response(
                    client=client, response=httpx.Response(status, json=example)
                )
                expected = (
                    "DryRunReport"
                    if example_name == "dryRun"
                    else ("PublishResult" if status == 200 else "Accepted")
                )
                assert type(parsed).__name__ == expected, example_name
        for model, example in (
            (models_shim.CancelResult, schema(spec, "CancelResult")["example"]),
            (models_shim.MediaImportReady, schema(spec, "MediaImportReady")["example"]),
        ):
            assert model.from_dict(example).to_dict() == example

    def test_the_generated_models_read_every_request_example(self, spec) -> None:
        examples = v2_operations(spec)[("POST", "/posts")]["op"]["requestBody"]["content"][
            "application/json"
        ]["examples"]
        for name, example in examples.items():
            value = example["value"]
            assert models_shim.PostRequest.from_dict(value).to_dict() == value, name


class TestGeneratedCode:
    def test_has_exactly_the_main_address_operations(self, spec) -> None:
        expected = {
            (found["op"]["tags"][0].lower(), snake(found["op"]["operationId"]))
            for found in v2_operations(spec).values()
        }
        package = importlib.import_module(f"{generated.__name__}.api")
        present = set()
        for tag in pkgutil.iter_modules(package.__path__):
            tag_package = importlib.import_module(f"{package.__name__}.{tag.name}")
            for module in pkgutil.iter_modules(tag_package.__path__):
                present.add((tag.name, module.name))
        assert present == expected

    def test_has_a_model_for_every_schema(self, spec) -> None:
        names = set(models_shim.__all__)
        for name in spec["components"]["schemas"]:
            if name.startswith("Older"):
                continue  # the older address's own shapes are left out (tools/v2_only.py)
            assert name in names or f"{name}_" in names, name

    def test_the_public_modules_re_export_all_of_it(self) -> None:
        assert set(models_shim.__all__) == set(generated.models.__all__)
        for tag in ("accounts", "media", "posts"):
            shim = getattr(api_shim, tag)
            tag_package = importlib.import_module(f"{generated.__name__}.api.{tag}")
            modules = {m.name for m in pkgutil.iter_modules(tag_package.__path__)}
            assert set(shim.__all__) == modules, tag
            for name in modules:
                assert hasattr(getattr(shim, name), "sync_detailed"), name

    def test_the_package_exports(self) -> None:
        for name in status200uploads.__all__:
            assert hasattr(status200uploads, name), name
