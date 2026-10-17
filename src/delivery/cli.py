"""`ad` — the hub's command-line tools, used by people and by the agent."""

from __future__ import annotations

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from delivery import __version__, doctor

app = typer.Typer(help="Agentic delivery hub tools.", no_args_is_help=True)
console = Console()

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
