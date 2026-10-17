"""Read, create and validate the hub's structured content (features, decisions, risks, roadmap)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from delivery import frontmatter
from delivery.models import Decision, Feature, Risk, Roadmap

PRD_PATH = Path("product/prd.md")
ROADMAP_PATH = Path("product/roadmap.yaml")


@dataclass(frozen=True)
class Kind:
    name: str
    model: type[BaseModel]
    directory: Path
    prefix: str

    def id_for(self, n: int) -> str:
        return f"{self.prefix}-{n:03d}"


KINDS = {
    k.name: k
    for k in (
        Kind("feature", Feature, Path("product/features"), "F"),
        Kind("decision", Decision, Path("kb/decisions"), "D"),
        Kind("risk", Risk, Path("kb/risks"), "R"),
    )
}


@dataclass(frozen=True)
class Doc:
    path: Path
    meta: BaseModel
    body: str


def template(name: str) -> str:
    return (files("delivery") / "templates" / f"{name}.md").read_text()


def slugify(title: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(slug) > max_len:
        cut = slug[: max_len + 1]
        # Prefer ending on a whole word; a single over-long word is truncated.
        slug = cut[: cut.rfind("-")] if "-" in cut else slug[:max_len]
    return slug or "untitled"


def _paths(root: Path, kind: Kind) -> list[Path]:
    return sorted((root / kind.directory).glob(f"{kind.prefix}-*.md"))


def load(root: Path, kind: Kind) -> list[Doc]:
    """Load all documents of a kind. Raises on the first invalid one; use `validate` to collect."""
    docs = []
    for path in _paths(root, kind):
        meta, body = frontmatter.parse(path.read_text())
        docs.append(Doc(path, kind.model.model_validate(meta), body))
    return docs


def load_roadmap(root: Path) -> Roadmap:
    path = root / ROADMAP_PATH
    if not path.is_file():
        return Roadmap()
    return Roadmap.model_validate(yaml.safe_load(path.read_text()) or {})


def next_id(root: Path, kind: Kind) -> str:
    numbers = [
        int(m.group(1))
        for p in _paths(root, kind)
        if (m := re.match(rf"{kind.prefix}-(\d+)", p.name))
    ]
    return kind.id_for(max(numbers, default=0) + 1)


def create(root: Path, kind: Kind, title: str) -> Path:
    doc_id = next_id(root, kind)
    meta = kind.model.model_validate({"id": doc_id, "title": title})
    path = root / kind.directory / f"{doc_id}-{slugify(title)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = frontmatter.render(meta.model_dump(mode="json", exclude_none=True), template(kind.name))
    path.write_text(text.replace("{{title}}", title))
    return path


def init_prd(root: Path, project_name: str, *, force: bool = False) -> Path:
    path = root / PRD_PATH
    if path.exists() and not force:
        raise FileExistsError(f"{PRD_PATH} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template("prd").replace("{{project}}", project_name))
    return path


def validate(root: Path) -> list[str]:
    """Check every structured document and cross-reference. Returns human-readable errors."""
    errors: list[str] = []
    ids: dict[str, Path] = {}
    features: list[Feature] = []

    for kind in KINDS.values():
        for path in _paths(root, kind):
            rel = path.relative_to(root)
            try:
                meta, _ = frontmatter.parse(path.read_text())
                model = kind.model.model_validate(meta)
            except (ValueError, ValidationError) as exc:
                errors.append(f"{rel}: {exc}")
                continue
            doc_id: str = getattr(model, "id")  # noqa: B009 - all kinds have an id
            if not path.name.startswith(doc_id + "-"):
                errors.append(f"{rel}: id {doc_id} does not match filename")
            if doc_id in ids:
                errors.append(f"{rel}: duplicate id {doc_id} (also {ids[doc_id]})")
            ids[doc_id] = rel
            if isinstance(model, Feature):
                features.append(model)

    milestones: set[str] | None
    try:
        milestones = {m.id for m in load_roadmap(root).milestones}
    except (yaml.YAMLError, ValidationError) as exc:
        errors.append(f"{ROADMAP_PATH}: {exc}")
        milestones = None  # already reported; don't cascade into every feature

    feature_ids = {f.id for f in features}
    for f in features:
        if f.milestone and milestones is not None and f.milestone not in milestones:
            errors.append(f"{f.id}: unknown milestone {f.milestone}")
        errors += [f"{f.id}: depends on unknown {d}" for d in f.depends_on if d not in feature_ids]
        story_ids = [s.id for s in f.stories]
        if len(story_ids) != len(set(story_ids)):
            errors.append(f"{f.id}: duplicate story ids")
    return errors
