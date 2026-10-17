"""Markdown documents with a YAML frontmatter block."""

from __future__ import annotations

from typing import Any

import yaml

DELIMITER = "---"


def parse(text: str) -> tuple[dict[str, Any], str]:
    """Split a document into (frontmatter, body). Documents without frontmatter get `{}`."""
    if not text.startswith(DELIMITER + "\n"):
        return {}, text
    end = text.find("\n" + DELIMITER + "\n", len(DELIMITER))
    if end == -1:
        raise ValueError("frontmatter block is not closed")
    meta = yaml.safe_load(text[len(DELIMITER) + 1 : end]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, text[end + len(DELIMITER) + 2 :].lstrip("\n")


def render(meta: dict[str, Any], body: str) -> str:
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    return f"{DELIMITER}\n{front}\n{DELIMITER}\n\n{body.strip()}\n"
