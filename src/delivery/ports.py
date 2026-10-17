"""Port interfaces that adapters implement.

Ports grow phase by phase; only the ones with a coded adapter are defined here.
Ports without a coded adapter yet are served through MCP (see CLAUDE.md).
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import PurePosixPath
from typing import ClassVar, Protocol, runtime_checkable

from delivery.config import Port


@runtime_checkable
class Adapter(Protocol):
    name: ClassVar[str]
    port: ClassVar[Port]
    # Environment variables that must be set for the adapter to work (checked by `ad doctor`).
    required_env: ClassVar[tuple[str, ...]]


@runtime_checkable
class StoragePort(Adapter, Protocol):
    """Read and write files in a document store (Drive, OneDrive, local folder...)."""

    def list(self, prefix: str = "") -> Iterator[PurePosixPath]: ...

    def read(self, path: PurePosixPath) -> bytes: ...

    def write(self, path: PurePosixPath, data: bytes) -> None: ...
