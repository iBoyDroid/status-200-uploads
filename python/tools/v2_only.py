"""Writes the part of openapi/openapi.yaml that the Python client is generated from.

openapi/openapi.yaml describes both addresses of the API: the main one
(https://status200uploads.com/api/v2, the file's top-level server) and the older one, whose paths
each carry a server of their own. This package calls only the main address. openapi-python-client
ignores path-level servers, so generated from the whole file it would send the older address's
requests to the main address.

So this keeps the paths without a server of their own, and drops the tags and components that only
the dropped paths use. Nothing else changes: every kept schema, parameter and response is copied as
it is. The canonical file is never edited; the result is JSON (no YAML anchors left) in python/build/,
which git ignores.

Usage: python tools/v2_only.py <openapi.yaml> <out.json>
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

COMPONENTS_PREFIX = "#/components/"
# Component kinds a document names by pointer. securitySchemes are named by key from `security`.
POINTED_KINDS = ("schemas", "responses", "parameters", "headers", "requestBodies", "examples")


def load(path: Path) -> dict[str, Any]:
    """The YAML file as plain data (YAML 1.2, like the generator's own reader)."""
    yaml = YAML(typ="safe", pure=True)
    data = yaml.load(path.read_text(encoding="utf-8"))
    # A JSON round trip turns YAML aliases into separate copies.
    return json.loads(json.dumps(data))


def is_older(path_item: dict[str, Any]) -> bool:
    """A path served on its own server: the older address."""
    return "servers" in path_item or path_item.get("x-status200-address") == "older"


def pointers(node: Any) -> Iterator[str]:
    """Every pointer into components in a node: $ref values, and the file's own
    x-status200-* entries that name a response ("response: '#/components/responses/...'")."""
    if isinstance(node, dict):
        for value in node.values():
            if isinstance(value, str) and value.startswith(COMPONENTS_PREFIX):
                yield value
            else:
                yield from pointers(value)
    elif isinstance(node, list):
        for value in node:
            yield from pointers(value)


def resolve(doc: dict[str, Any], pointer: str) -> Any:
    at: Any = doc
    for raw in pointer[2:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(at, dict) or key not in at:
            raise KeyError(f"unresolved pointer {pointer}")
        at = at[key]
    return at


def reachable(doc: dict[str, Any], roots: Any) -> set[str]:
    """Every component pointer reachable from the roots, through the components themselves."""
    reached: set[str] = set()
    stack = list(pointers(roots))
    while stack:
        pointer = stack.pop()
        if pointer in reached:
            continue
        reached.add(pointer)
        stack.extend(pointers(resolve(doc, pointer)))
    return reached


def v2_only(doc: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """The main address's part of the document, and what was dropped."""
    out = json.loads(json.dumps(doc))
    dropped: dict[str, list[str]] = {"paths": [], "tags": []}

    kept_paths = {}
    older_paths = {}
    for path, item in out["paths"].items():
        if is_older(item):
            dropped["paths"].append(path)
            older_paths[path] = item
        else:
            kept_paths[path] = item
    out["paths"] = kept_paths

    used_tags = {
        tag
        for item in kept_paths.values()
        for operation in item.values()
        if isinstance(operation, dict)
        for tag in operation.get("tags", [])
    }
    kept_tags = []
    for tag in out.get("tags", []):
        (kept_tags if tag["name"] in used_tags else dropped["tags"]).append(tag)
    out["tags"] = kept_tags
    dropped["tags"] = [tag["name"] for tag in dropped["tags"]]

    # A component goes only when the dropped paths reach it and the rest of the document does not.
    # Components nothing points at (e.g. the per-network posting options, named in
    # x-status200-options-by-platform) stay: they are part of the API's description.
    kept_roots = {key: value for key, value in out.items() if key != "components"}
    used_by_rest = reachable(out, kept_roots)
    used_by_older = reachable(out, older_paths)
    only_older = used_by_older - used_by_rest

    components = out.get("components", {})
    for kind in POINTED_KINDS:
        entries = components.get(kind)
        if not isinstance(entries, dict):
            continue
        for name in list(entries):
            if f"{COMPONENTS_PREFIX}{kind}/{name}" in only_older:
                del entries[name]
                dropped.setdefault(kind, []).append(name)

    # Every pointer left must resolve.
    for pointer in pointers(out):
        resolve(out, pointer)
    return out, dropped


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    source, target = Path(argv[1]), Path(argv[2])
    doc, dropped = v2_only(load(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    operations = sum(
        1
        for item in doc["paths"].values()
        for method in ("get", "put", "post", "delete", "patch")
        if method in item
    )
    print(f"{target}: {len(doc['paths'])} paths, {operations} operations of the main address")
    for kind, names in dropped.items():
        if names:
            print(f"  dropped {kind}: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
