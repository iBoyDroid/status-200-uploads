"""The package as it is published: version, metadata, dependencies, license and typing marker."""

from __future__ import annotations

import ast
import re
import sys
import tomllib

from conftest import REPO

import status200uploads
from status200uploads import USER_AGENT, __version__

PYTHON = REPO / "python"
PACKAGE = PYTHON / "src" / "status200uploads"
PYPROJECT = tomllib.loads((PYTHON / "pyproject.toml").read_text(encoding="utf-8"))
PROJECT = PYPROJECT["project"]


def test_the_version_is_the_same_everywhere() -> None:
    assert PROJECT["version"] == __version__
    assert USER_AGENT == f"status200uploads-python/{__version__}"
    changelog = (PYTHON / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## {__version__}" in changelog


def test_metadata() -> None:
    assert PROJECT["name"] == "status200uploads"
    assert PROJECT["requires-python"] == ">=3.11"
    assert PROJECT["license"] == "MIT"
    assert PROJECT["license-files"] == ["LICENSE"]
    assert PROJECT["authors"] == [{"name": "iBoyDroid", "email": "info@status200uploads.com"}]
    urls = PROJECT["urls"]
    assert urls["Source"] == "https://github.com/iBoyDroid/status-200-uploads/tree/main/python"
    assert urls["Documentation"] == "https://status200uploads.com/docs/api#guide-python"
    assert PROJECT["readme"] == "README.md"
    # A license expression (PEP 639) rules out the old license classifier.
    assert not [c for c in PROJECT["classifiers"] if c.startswith("License ::")]


def test_the_license_is_the_repositorys() -> None:
    assert (PYTHON / "LICENSE").read_text(encoding="utf-8") == (REPO / "LICENSE").read_text(
        encoding="utf-8"
    )


def test_it_is_typed() -> None:
    assert (PACKAGE / "py.typed").exists()


def _third_party_imports() -> set[str]:
    stdlib = set(sys.stdlib_module_names)
    found: set[str] = set()
    for path in PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                if top not in stdlib and top not in ("__future__", "status200uploads"):
                    found.add(top)
    return found


def test_the_dependencies_are_exactly_what_the_code_imports() -> None:
    declared = {
        requirement.split(">")[0].split("=")[0].split("<")[0].strip().lower()
        for requirement in PROJECT["dependencies"]
    }
    assert _third_party_imports() == declared == {"httpx", "attrs"}


def test_the_generated_code_needs_no_typing_extensions() -> None:
    # ruff targets Python 3.11 ([tool.ruff] in pyproject.toml), so typing.Self stays typing.Self.
    assert "typing_extensions" not in _third_party_imports()


def test_the_readme_examples_use_only_what_exists() -> None:
    readme = (PYTHON / "README.md").read_text(encoding="utf-8")
    blocks = [block.split("```", 1)[0] for block in readme.split("```python\n")[1:]]
    assert blocks, "the README has Python examples"
    methods = {name for name in dir(status200uploads.Status200) if not name.startswith("_")}
    exported = set(status200uploads.__all__)
    for block in blocks:
        tree = ast.parse(block)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "s200"
            ):
                assert node.attr in methods, node.attr
            if isinstance(node, ast.ImportFrom) and node.module == "status200uploads":
                for alias in node.names:
                    assert alias.name in exported, alias.name
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("status200uploads.")
            ):
                module = __import__(node.module, fromlist=[a.name for a in node.names])
                for alias in node.names:
                    assert hasattr(module, alias.name), f"{node.module}.{alias.name}"


def test_nothing_shaped_like_a_key_is_in_the_package_or_its_docs() -> None:
    key_like = re.compile(r"rl_[0-9A-Za-z]{8,}")
    for path in [PYTHON / "README.md", PYTHON / "CHANGELOG.md", *PACKAGE.rglob("*.py")]:
        assert not key_like.search(path.read_text(encoding="utf-8")), path
