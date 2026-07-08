from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from ofks.io import read_jsonl, write_jsonl

app = typer.Typer(help="Combine JSONL workflow records with duplicate-id protection.")
console = Console()


@app.command()
def main(
    records: list[Path] = typer.Option(
        ...,
        "--records",
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="JSONL records to combine. Can be repeated.",
    ),
    out: Path = typer.Option(..., "--out", file_okay=True, dir_okay=False),
    id_key: str = typer.Option("structure_id", "--id-key"),
) -> None:
    combined = combine_record_sets([read_jsonl(path) for path in records], id_key=id_key)
    count = write_jsonl(out, combined)
    console.print(f"Wrote {count} combined records to {out}")


def combine_record_sets(record_sets: list[list[dict[str, Any]]], id_key: str = "structure_id") -> list[dict[str, Any]]:
    combined: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for record_set in record_sets:
        for record in record_set:
            record_id = record.get(id_key)
            if record_id is not None:
                record_id_text = str(record_id)
                if record_id_text in seen_ids:
                    raise ValueError(f"Duplicate {id_key}: {record_id_text}")
                seen_ids.add(record_id_text)
            combined.append(dict(record))
    return combined


if __name__ == "__main__":
    app()
