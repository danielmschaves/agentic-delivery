"""Adapter discovery via the `delivery.adapters` entry-point group."""

from __future__ import annotations

from importlib.metadata import entry_points

from delivery.ports import Adapter

GROUP = "delivery.adapters"


def available() -> dict[str, type[Adapter]]:
    """All installed adapters, keyed by entry-point name."""
    return {ep.name: ep.load() for ep in entry_points(group=GROUP)}


def get(name: str) -> type[Adapter]:
    try:
        return available()[name]
    except KeyError:
        raise LookupError(f"No adapter named {name!r} is installed") from None
