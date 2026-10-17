from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from typer.testing import CliRunner

from delivery import __version__
from delivery.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_doctor_ok(make_hub: Callable[..., Path], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(make_hub())
    assert runner.invoke(app, ["doctor"]).exit_code == 0


def test_doctor_fails_without_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert runner.invoke(app, ["doctor"]).exit_code == 1
