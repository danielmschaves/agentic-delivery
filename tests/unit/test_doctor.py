from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

import pytest

from delivery import adapters, doctor
from delivery.adapters.local_fs import LocalFsStorage
from delivery.config import Port


class FakeTracker:
    name: ClassVar[str] = "fake_tracker"
    port: ClassVar[Port] = Port.TRACKER
    required_env: ClassVar[tuple[str, ...]] = ("FAKE_TOKEN",)


@pytest.fixture(autouse=True)
def _fake_adapters(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        adapters, "available", lambda: {"local_fs": LocalFsStorage, "fake_tracker": FakeTracker}
    )


def _by_name(checks: list[doctor.Check]) -> dict[str, doctor.Check]:
    return {c.name: c for c in checks}


def test_healthy(make_hub: Callable[..., Path]) -> None:
    checks = _by_name(doctor.run(make_hub()))
    assert checks["config"].status is doctor.Status.OK
    assert checks["port:storage"].status is doctor.Status.OK
    assert checks["port:tracker"].status is doctor.Status.WARN


def test_port_failures(make_hub: Callable[..., Path], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FAKE_TOKEN", raising=False)
    hub = make_hub(
        "project: {name: x, client: y, key: AB}\n"
        "integrations:\n"
        "  tracker: {adapter: fake_tracker}\n"
        "  storage: {adapter: fake_tracker}\n"
        "  wiki: {adapter: ghost}\n"
        "  mail: {adapter: mcp}\n"
    )
    checks = _by_name(doctor.run(hub))
    assert "missing env: FAKE_TOKEN" in checks["port:tracker"].detail
    assert "serves tracker" in checks["port:storage"].detail
    assert "not installed" in checks["port:wiki"].detail
    assert checks["port:mail"].detail == "via MCP"

    monkeypatch.setenv("FAKE_TOKEN", "t")
    assert _by_name(doctor.run(hub))["port:tracker"].status is doctor.Status.OK


def test_missing_config(tmp_path: Path) -> None:
    checks = _by_name(doctor.run(tmp_path))
    assert checks["config"].status is doctor.Status.FAIL
