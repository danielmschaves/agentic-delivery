"""Storage adapter backed by a local directory. Default for new hubs and tests."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path, PurePosixPath
from typing import ClassVar

from delivery.config import Port


class LocalFsStorage:
    name: ClassVar[str] = "local_fs"
    port: ClassVar[Port] = Port.STORAGE
    required_env: ClassVar[tuple[str, ...]] = ()

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _resolve(self, path: PurePosixPath) -> Path:
        full = (self.root / path).resolve()
        if not full.is_relative_to(self.root):
            raise ValueError(f"{path} escapes storage root")
        return full

    def list(self, prefix: str = "") -> Iterator[PurePosixPath]:
        base = self._resolve(PurePosixPath(prefix))
        if not base.exists():
            return
        for p in sorted(base.rglob("*")):
            if p.is_file():
                yield PurePosixPath(p.relative_to(self.root).as_posix())

    def read(self, path: PurePosixPath) -> bytes:
        return self._resolve(path).read_bytes()

    def write(self, path: PurePosixPath, data: bytes) -> None:
        full = self._resolve(path)
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(data)
