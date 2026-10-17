from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from pydantic import ValidationError

from delivery.config import NONE, Port, find_root, load_config


def test_load_minimal(make_hub: Callable[..., Path]) -> None:
    config = load_config(make_hub())
    assert config.project.key == "TH"
    assert config.binding(Port.STORAGE).adapter == "local_fs"
    assert config.binding(Port.TRACKER).adapter == NONE


def test_find_root_walks_up(make_hub: Callable[..., Path]) -> None:
    root = make_hub()
    nested = root / "a" / "b"
    nested.mkdir(parents=True)
    assert find_root(nested) == root.resolve()


def test_find_root_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        find_root(tmp_path)


@pytest.mark.parametrize(
    "config",
    [
        "project: {name: x, client: y, key: lower}\n",
        "project: {name: x, client: y, key: AB}\nintegrations: {nope: {adapter: mcp}}\n",
        "project: {name: x, client: y, key: AB, extra: 1}\n",
    ],
)
def test_invalid_config(make_hub: Callable[..., Path], config: str) -> None:
    with pytest.raises(ValidationError):
        load_config(make_hub(config))


def test_repo_config_is_valid() -> None:
    load_config(Path(__file__).parents[2])
