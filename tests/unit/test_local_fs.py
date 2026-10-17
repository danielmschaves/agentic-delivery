from __future__ import annotations

from pathlib import Path, PurePosixPath

import pytest

from delivery import adapters
from delivery.adapters.local_fs import LocalFsStorage
from delivery.ports import StoragePort


def test_roundtrip_and_list(tmp_path: Path) -> None:
    store = LocalFsStorage(tmp_path)
    store.write(PurePosixPath("a/b.md"), b"hello")
    store.write(PurePosixPath("c.txt"), b"x")
    assert store.read(PurePosixPath("a/b.md")) == b"hello"
    assert list(store.list()) == [PurePosixPath("a/b.md"), PurePosixPath("c.txt")]
    assert list(store.list("a")) == [PurePosixPath("a/b.md")]
    assert list(store.list("missing")) == []


def test_rejects_escape(tmp_path: Path) -> None:
    store = LocalFsStorage(tmp_path / "root")
    with pytest.raises(ValueError, match="escapes"):
        store.write(PurePosixPath("../outside"), b"x")


def test_conforms_to_port(tmp_path: Path) -> None:
    assert isinstance(LocalFsStorage(tmp_path), StoragePort)


def test_registered_via_entry_point() -> None:
    assert adapters.get("local_fs") is LocalFsStorage
    with pytest.raises(LookupError):
        adapters.get("does-not-exist")
