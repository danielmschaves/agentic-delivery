from __future__ import annotations

import pytest

from delivery import frontmatter


def test_roundtrip() -> None:
    text = frontmatter.render({"id": "F-001", "title": "Ünïcode"}, "\n# Body\n\ntext\n")
    assert frontmatter.parse(text) == ({"id": "F-001", "title": "Ünïcode"}, "# Body\n\ntext\n")


def test_no_frontmatter() -> None:
    assert frontmatter.parse("# Just markdown\n") == ({}, "# Just markdown\n")


@pytest.mark.parametrize("text", ["---\nid: 1\n", "---\n- a\n- b\n---\nbody\n"])
def test_malformed(text: str) -> None:
    with pytest.raises(ValueError):
        frontmatter.parse(text)
