"""Health checks for a hub: config validity, adapter availability, credentials, tooling."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from pydantic import ValidationError

from delivery import adapters
from delivery.config import MCP, NONE, Port, find_root, load_config

REQUIRED_TOOLS = ("git", "uv")


class Status(StrEnum):
    OK = "ok"
    WARN = "warn"
    FAIL = "fail"


@dataclass(frozen=True)
class Check:
    name: str
    status: Status
    detail: str = ""


def run(start: Path | None = None) -> list[Check]:
    checks = [
        Check(f"tool:{tool}", Status.OK if shutil.which(tool) else Status.FAIL)
        for tool in REQUIRED_TOOLS
    ]

    try:
        root = find_root(start)
        config = load_config(root)
    except (FileNotFoundError, ValidationError) as exc:
        return [*checks, Check("config", Status.FAIL, str(exc))]
    checks.append(Check("config", Status.OK, f"{config.project.name} ({root})"))

    installed = adapters.available()
    for port in Port:
        binding = config.binding(port)
        name = f"port:{port}"
        if binding.adapter == NONE:
            checks.append(Check(name, Status.WARN, "not configured"))
        elif binding.adapter == MCP:
            checks.append(Check(name, Status.OK, "via MCP"))
        elif (cls := installed.get(binding.adapter)) is None:
            checks.append(Check(name, Status.FAIL, f"adapter {binding.adapter!r} not installed"))
        elif cls.port != port:
            checks.append(
                Check(name, Status.FAIL, f"adapter {binding.adapter!r} serves {cls.port}")
            )
        elif missing := [v for v in cls.required_env if not os.environ.get(v)]:
            checks.append(Check(name, Status.FAIL, f"missing env: {', '.join(missing)}"))
        else:
            checks.append(Check(name, Status.OK, binding.adapter))
    return checks
