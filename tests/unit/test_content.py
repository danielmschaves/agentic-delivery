from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from delivery import content, frontmatter
from delivery.models import Feature

FEATURE = content.KINDS["feature"]


@pytest.fixture
def hub(make_hub: Callable[..., Path]) -> Path:
    return make_hub()


def _write_feature(hub: Path, name: str, **meta: object) -> None:
    path = hub / "product/features" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.render(meta, "# body"))


def test_slugify() -> None:
    assert content.slugify("Repo linking: GitHub & ADO!") == "repo-linking-github-ado"
    assert content.slugify("???") == "untitled"
    assert len(content.slugify("x" * 80)) == 50
    assert content.slugify("alpha " * 10, max_len=20) == "alpha-alpha-alpha"


def test_create_assigns_sequential_ids(hub: Path) -> None:
    first = content.create(hub, FEATURE, "Product repo linking")
    second = content.create(hub, FEATURE, "Tracker sync")
    assert first.name == "F-001-product-repo-linking.md"
    assert second.name == "F-002-tracker-sync.md"

    meta, body = frontmatter.parse(second.read_text())
    assert meta == {
        "id": "F-002",
        "title": "Tracker sync",
        "status": "proposed",
        "priority": "should",
        "depends_on": [],
        "stories": [],
        "tracker": {},
    }
    assert body.startswith("# Tracker sync\n")


@pytest.mark.parametrize("kind", ["decision", "risk"])
def test_create_other_kinds(hub: Path, kind: str) -> None:
    path = content.create(hub, content.KINDS[kind], "Something")
    assert path.parent == hub / content.KINDS[kind].directory
    assert content.load(hub, content.KINDS[kind])[0].meta.model_dump()["title"] == "Something"


def test_load(hub: Path) -> None:
    content.create(hub, FEATURE, "A")
    [doc] = content.load(hub, FEATURE)
    assert isinstance(doc.meta, Feature)
    assert doc.meta.id == "F-001"


def test_prd_init(hub: Path) -> None:
    path = content.init_prd(hub, "Acme")
    assert path.read_text().startswith("# Acme — Product Requirements")
    with pytest.raises(FileExistsError):
        content.init_prd(hub, "Acme")
    content.init_prd(hub, "Other", force=True)
    assert "Other" in path.read_text()


def test_validate_clean(hub: Path) -> None:
    (hub / "product").mkdir()
    (hub / "product/roadmap.yaml").write_text("milestones:\n  - {id: M1, title: First}\n")
    _write_feature(hub, "F-001-a.md", id="F-001", title="A", milestone="M1")
    _write_feature(
        hub,
        "F-002-b.md",
        id="F-002",
        title="B",
        depends_on=["F-001"],
        stories=[{"id": "S1", "title": "s"}, {"id": "S2", "title": "t"}],
    )
    assert content.validate(hub) == []


def test_validate_reports_everything(hub: Path) -> None:
    _write_feature(hub, "F-001-a.md", id="F-001", title="A", milestone="M9", depends_on=["F-404"])
    _write_feature(hub, "F-002-b.md", id="F-001", title="dup id, wrong filename")
    _write_feature(hub, "F-003-c.md", id="F-003", title="C", priority="urgent")
    _write_feature(
        hub,
        "F-004-d.md",
        id="F-004",
        title="D",
        stories=[{"id": "S1", "title": "x"}, {"id": "S1", "title": "y"}],
    )
    (hub / "product/roadmap.yaml").write_text("milestones: [{id: bad}]\n")

    errors = "\n".join(content.validate(hub))
    for expected in [
        "F-001: depends on unknown F-404",
        "F-002-b.md: id F-001 does not match filename",
        "duplicate id F-001",
        "F-003-c.md:",
        "F-004: duplicate story ids",
        "roadmap.yaml:",
    ]:
        assert expected in errors


def test_unknown_milestone(hub: Path) -> None:
    _write_feature(hub, "F-001-a.md", id="F-001", title="A", milestone="M9")
    assert content.validate(hub) == ["F-001: unknown milestone M9"]


def test_invalid_roadmap_does_not_cascade(hub: Path) -> None:
    _write_feature(hub, "F-001-a.md", id="F-001", title="A", milestone="M9")
    (hub / "product/roadmap.yaml").write_text("milestones: [{id: bad}]\n")
    [error] = content.validate(hub)
    assert error.startswith("product/roadmap.yaml:")
