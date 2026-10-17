"""Hub configuration: `project.yaml` at the repo root, validated with pydantic."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

CONFIG_FILE = "project.yaml"

# Reserved adapter names that don't map to coded adapters.
NONE = "none"  # port disabled
MCP = "mcp"  # handled interactively by the agent through an MCP server


class Port(StrEnum):
    TRACKER = "tracker"
    WIKI = "wiki"
    STORAGE = "storage"
    MAIL = "mail"
    CALENDAR = "calendar"
    MEETINGS = "meetings"
    REPOS = "repos"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProjectInfo(_Strict):
    name: str
    client: str
    key: str = Field(pattern=r"^[A-Z][A-Z0-9]{1,9}$", description="Short project key, e.g. AD")


class Binding(_Strict):
    """Which adapter fills a port, plus adapter-specific options."""

    adapter: str = NONE
    options: dict[str, Any] = Field(default_factory=dict)


class HubConfig(_Strict):
    project: ProjectInfo
    integrations: dict[Port, Binding] = Field(default_factory=dict)

    def binding(self, port: Port) -> Binding:
        return self.integrations.get(port, Binding())


def find_root(start: Path | None = None) -> Path:
    """Walk up from `start` to the directory holding project.yaml."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / CONFIG_FILE).is_file():
            return candidate
    raise FileNotFoundError(f"{CONFIG_FILE} not found in {here} or any parent")


def load_config(root: Path) -> HubConfig:
    raw = yaml.safe_load((root / CONFIG_FILE).read_text()) or {}
    return HubConfig.model_validate(raw)
