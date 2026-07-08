from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ofks.reports.summary import build_summary, render_summary_markdown

app = typer.Typer(help="Summarize workflow state into a Markdown report.")
console = Console()


@app.command()
def main(
    system: str = typer.Option(..., "--system"),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    candidates: Path | None = typer.Option(None, "--candidates", file_okay=True, dir_okay=False),
    fast_screen: Path | None = typer.Option(None, "--fast-screen", file_okay=True, dir_okay=False),
    selected: Path | None = typer.Option(None, "--selected", file_okay=True, dir_okay=False),
    manifest: Path | None = typer.Option(None, "--manifest", file_okay=True, dir_okay=False),
    parsed: Path | None = typer.Option(None, "--parsed", file_okay=True, dir_okay=False),
    predictions: Path | None = typer.Option(None, "--predictions", file_okay=True, dir_okay=False),
    delta_report: Path | None = typer.Option(None, "--delta-report", file_okay=True, dir_okay=False),
) -> None:
    summary = build_summary(
        system=system,
        candidates=candidates,
        fast_screen=fast_screen,
        selected=selected,
        manifest=manifest,
        parsed=parsed,
        predictions=predictions,
        delta_report=delta_report,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_summary_markdown(summary), encoding="utf-8")
    console.print(f"Wrote summary report to {out}")


if __name__ == "__main__":
    app()
