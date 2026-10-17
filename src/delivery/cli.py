"""`ad` — the hub's command-line tools, used by people and by the agent."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from delivery import __version__, content, doctor
from delivery.config import find_root, load_config

app = typer.Typer(help="Agentic delivery hub tools.", no_args_is_help=True)
prd_app = typer.Typer(help="Product requirements document.", no_args_is_help=True)
app.add_typer(prd_app, name="prd")
console = Console()

KindName = StrEnum("KindName", {k: k for k in content.KINDS})  # type: ignore[misc]


def _root() -> Path:
    try:
        return find_root()
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/]")
        raise typer.Exit(1) from None


def _rel(path: Path) -> str:
    return str(path.relative_to(Path.cwd().resolve(), walk_up=True))


_STYLE = {doctor.Status.OK: "green", doctor.Status.WARN: "yellow", doctor.Status.FAIL: "red"}


@app.callback()
def _main() -> None:
    load_dotenv()


@app.command()
def version() -> None:
    """Print the tooling version."""
    console.print(__version__)


@app.command("doctor")
def doctor_cmd() -> None:
    """Check config, adapters, credentials and required tools."""
    checks = doctor.run()
    table = Table("check", "status", "detail")
    for c in checks:
        table.add_row(c.name, f"[{_STYLE[c.status]}]{c.status}[/]", c.detail)
    console.print(table)
    if any(c.status is doctor.Status.FAIL for c in checks):
        raise typer.Exit(1)


@app.command()
def new(
    kind: Annotated[KindName, typer.Argument(help="What to create")],
    title: Annotated[str, typer.Argument(help="Title of the new document")],
) -> None:
    """Create a feature, decision or risk from its template, with the next free id."""
    path = content.create(_root(), content.KINDS[kind.value], title)
    console.print(_rel(path))


@app.command("list")
def list_cmd(
    kind: Annotated[KindName, typer.Argument(help="What to list")],
    status: Annotated[str | None, typer.Option(help="Only show this status")] = None,
) -> None:
    """List features, decisions or risks."""
    docs = content.load(_root(), content.KINDS[kind.value])
    table = Table("id", "title", "status", "file")
    for doc in docs:
        meta = doc.meta.model_dump()
        if status is None or meta["status"] == status:
            table.add_row(meta["id"], meta["title"], meta["status"], _rel(doc.path))
    console.print(table)


@app.command()
def validate() -> None:
    """Validate structured content: schemas, ids and cross-references."""
    errors = content.validate(_root())
    for error in errors:
        console.print(f"[red]✗[/] {error}")
    if errors:
        raise typer.Exit(1)
    console.print("[green]content valid[/]")


@prd_app.command("init")
def prd_init(
    force: Annotated[bool, typer.Option(help="Overwrite an existing PRD")] = False,
) -> None:
    """Create product/prd.md from the PRD template."""
    root = _root()
    try:
        path = content.init_prd(root, load_config(root).project.name, force=force)
    except FileExistsError as exc:
        console.print(f"[yellow]{exc}[/] (use --force to overwrite)")
        raise typer.Exit(1) from None
    console.print(_rel(path))
