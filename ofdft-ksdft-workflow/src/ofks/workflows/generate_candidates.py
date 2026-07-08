from __future__ import annotations

from pathlib import Path

import typer
from ase.io import write
from rich.console import Console

from ofks.config import load_system_config
from ofks.structures.placements import generate_adsorption_candidates

app = typer.Typer(help="Generate slab-adsorbate candidate structures.")
console = Console()


@app.command()
def main(
    system: Path = typer.Option(..., "--system", exists=True, file_okay=True, dir_okay=False),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
) -> None:
    config = load_system_config(system)
    candidates = generate_adsorption_candidates(config)
    for atoms in candidates:
        atoms.info.pop("adsorbate_info", None)
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, candidates)
    console.print(f"Wrote {len(candidates)} candidates to {out}")


if __name__ == "__main__":
    app()
