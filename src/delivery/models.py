"""Canonical product and knowledge models.

These are the source of truth that trackers sync against and renderers export from. Features,
decisions and risks are Markdown files whose frontmatter is the model (the body is free text);
milestones live in `product/roadmap.yaml`.
"""

from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class Status(StrEnum):
    PROPOSED = "proposed"
    DEFINED = "defined"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    DROPPED = "dropped"


class Priority(StrEnum):
    """MoSCoW."""

    MUST = "must"
    SHOULD = "should"
    COULD = "could"
    WONT = "wont"


class Story(_Strict):
    id: str = Field(pattern=r"^S\d+$", description="Unique within its feature, e.g. S1")
    title: str
    status: Status = Status.PROPOSED
    tracker: dict[str, str] = Field(default_factory=dict)


class Feature(_Strict):
    id: str = Field(pattern=r"^F-\d{3}$")
    title: str
    status: Status = Status.PROPOSED
    priority: Priority = Priority.SHOULD
    milestone: str | None = None
    owner: str | None = None
    depends_on: list[str] = Field(default_factory=list)
    stories: list[Story] = Field(default_factory=list)
    # External references, e.g. {"jira": "ACME-12"} or {"ado": "4711"}.
    tracker: dict[str, str] = Field(default_factory=dict)


class DecisionStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    SUPERSEDED = "superseded"


class Decision(_Strict):
    id: str = Field(pattern=r"^D-\d{3}$")
    title: str
    status: DecisionStatus = DecisionStatus.PROPOSED
    decided: date | None = None
    source: str | None = None


class Level(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskStatus(StrEnum):
    OPEN = "open"
    MITIGATED = "mitigated"
    CLOSED = "closed"


class Risk(_Strict):
    id: str = Field(pattern=r"^R-\d{3}$")
    title: str
    status: RiskStatus = RiskStatus.OPEN
    likelihood: Level = Level.MEDIUM
    impact: Level = Level.MEDIUM
    owner: str | None = None


class Milestone(_Strict):
    id: str = Field(pattern=r"^M\d+$")
    title: str
    status: Status = Status.PROPOSED
    target: date | None = None


class Roadmap(_Strict):
    milestones: list[Milestone] = Field(default_factory=list)
