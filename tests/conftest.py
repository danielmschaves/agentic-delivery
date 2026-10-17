from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

MINIMAL = """\
project:
  name: Test Hub
  client: test
  key: TH
integrations:
  storage: { adapter: local_fs }
"""


@pytest.fixture
def make_hub(tmp_path: Path) -> Callable[[str], Path]:
    def _make(config: str = MINIMAL) -> Path:
        (tmp_path / "project.yaml").write_text(config)
        return tmp_path

    return _make
