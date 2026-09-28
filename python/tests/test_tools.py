"""tools/v2_only.py, which writes the part of the OpenAPI file the client is generated from."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
from conftest import SPEC_PATH

TOOL = Path(__file__).resolve().parents[1] / "tools" / "v2_only.py"


@pytest.fixture(scope="module")
def tool():
    spec = importlib.util.spec_from_file_location("v2_only", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def filtered(tool):
    return tool.v2_only(tool.load(SPEC_PATH))


def test_keeps_the_main_address_paths_and_drops_the_older_ones(tool, filtered, spec) -> None:
    doc, dropped = filtered
    main = {path for path, item in spec["paths"].items() if "servers" not in item}
    older = {path for path, item in spec["paths"].items() if "servers" in item}
    assert set(doc["paths"]) == main
    assert set(dropped["paths"]) == older
    assert all("servers" not in item for item in doc["paths"].values())
    assert doc["servers"] == spec["servers"]


def test_kept_paths_are_copied_as_they_are(filtered, spec) -> None:
    doc, _ = filtered
    for path, item in doc["paths"].items():
        assert item == spec["paths"][path]


def test_drops_only_what_the_older_paths_alone_use(filtered, spec) -> None:
    doc, dropped = filtered
    assert set(dropped["schemas"]) == {"OlderErrorObject", "OlderErrorResponse"}
    assert set(dropped["responses"]) == {
        "OlderMethodNotAllowed",
        "OlderDefault",
        "OlderMediaDefault",
    }
    assert dropped["tags"] == ["Older address"]
    # Schemas nothing points at stay (the per-network posting options, named by
    # x-status200-options-by-platform).
    for name in spec["components"]["schemas"]["NetworkOptions"][
        "x-status200-options-by-platform"
    ].values():
        assert name in doc["components"]["schemas"], name
    kept = set(spec["components"]["schemas"]) - set(dropped["schemas"])
    assert set(doc["components"]["schemas"]) == kept
    for name in kept:
        assert doc["components"]["schemas"][name] == spec["components"]["schemas"][name], name
    # The retry table and the file's other extensions travel along.
    assert doc["components"]["x-status200-retry"] == spec["components"]["x-status200-retry"]


def test_every_pointer_left_resolves(tool, filtered) -> None:
    doc, _ = filtered
    for pointer in tool.pointers(doc):
        tool.resolve(doc, pointer)


def test_filtering_twice_changes_nothing(tool, filtered) -> None:
    doc, _ = filtered
    again, dropped = tool.v2_only(doc)
    assert again == doc
    assert all(not names for names in dropped.values())


def test_writes_json(tool, tmp_path) -> None:
    target = tmp_path / "build" / "openapi-v2.json"
    assert tool.main(["v2_only.py", str(SPEC_PATH), str(target)]) == 0
    written = json.loads(target.read_text(encoding="utf-8"))
    assert written["openapi"] == "3.1.0"
    assert "/api-posts" not in written["paths"]
