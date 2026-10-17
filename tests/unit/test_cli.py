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


def test_content_workflow(make_hub: Callable[..., Path], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(make_hub())

    result = runner.invoke(app, ["new", "feature", "Repo linking"])
    assert result.exit_code == 0
    assert "F-001-repo-linking.md" in result.stdout

    result = runner.invoke(app, ["list", "feature"])
    assert "Repo linking" in result.stdout
    assert "Repo linking" not in runner.invoke(app, ["list", "feature", "--status", "done"]).stdout

    assert runner.invoke(app, ["validate"]).exit_code == 0
    Path("product/features/F-002-broken.md").write_text("---\nid: nope\n---\n")
    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 1
    assert "F-002-broken.md" in result.stdout


def test_prd_init(make_hub: Callable[..., Path], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(make_hub())
    assert runner.invoke(app, ["prd", "init"]).exit_code == 0
    assert Path("product/prd.md").read_text().startswith("# Test Hub")
    assert runner.invoke(app, ["prd", "init"]).exit_code == 1
    assert runner.invoke(app, ["prd", "init", "--force"]).exit_code == 0


def test_requires_hub(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert runner.invoke(app, ["validate"]).exit_code == 1
