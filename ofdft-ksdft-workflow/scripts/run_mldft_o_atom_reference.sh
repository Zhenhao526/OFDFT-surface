#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRUCTURES25_DIR="${STRUCTURES25_DIR:-/mnt/afs/home/xiazhenhao/dft/structures25}"
OUT_DIR="${OUT_DIR:-$ROOT_DIR/data/reports/benchmarks/mofdft_o_atom_real_$(date +%Y%m%d_%H%M%S)}"
MODEL="${MODEL:-str25_qm9}"
DEVICE="${DEVICE:-cuda}"
TRANSFORM_DEVICE="${TRANSFORM_DEVICE:-cpu}"
MAX_CYCLE="${MAX_CYCLE:-5000}"
CONVERGENCE_TOLERANCE="${CONVERGENCE_TOLERANCE:-1e-4}"
LEARNING_RATE="${LEARNING_RATE:-1e-3}"
CHARGE="${CHARGE:-0}"
export MODEL CHARGE

MLDFT_PYTHON="$STRUCTURES25_DIR/.venv/bin/python"
MLDFT_CLI="$STRUCTURES25_DIR/.venv/bin/mldft"
export DFT_DATA="${DFT_DATA:-$STRUCTURES25_DIR/_runtime/data}"
export DFT_MODELS="${DFT_MODELS:-$STRUCTURES25_DIR/_runtime/models}"

mkdir -p "$OUT_DIR"

cat > "$OUT_DIR/o_atom.xyz" <<EOF
1
O atom closed-shell MLDFT diagnostic, charge=${CHARGE}
O 0.000000 0.000000 0.000000
EOF

(
  cd "$STRUCTURES25_DIR"
  "$MLDFT_CLI" "$OUT_DIR/o_atom.xyz" \
    --charge "$CHARGE" \
    --model "$MODEL" \
    --device "$DEVICE" \
    --transform-device "$TRANSFORM_DEVICE" \
    --max-cycle "$MAX_CYCLE" \
    --convergence-tolerance "$CONVERGENCE_TOLERANCE" \
    --learning-rate "$LEARNING_RATE"
) > "$OUT_DIR/o_atom_mldft.stdout" 2>&1

ENERGY_EV="$("$MLDFT_PYTHON" - "$OUT_DIR" <<'PY'
import json
import os
import pathlib
import re
import sys

import torch

hartree_to_ev = 27.211386245988
out = pathlib.Path(sys.argv[1])
sample = torch.load(out / "o_atom.pt", map_location="cpu", weights_only=False)
energies = sample.energies
stdout = (out / "o_atom_mldft.stdout").read_text(errors="ignore")
grad_matches = re.findall(r"grad_norm=([0-9.]+e[+-][0-9]+)", stdout)
summary = {
    "method": "mldft",
    "model": os.environ.get("MODEL", "str25_qm9"),
    "formula": "O",
    "charge": int(os.environ.get("CHARGE", "0")),
    "spin_note": (
        "mldft CLI exposes charge but not spin. This neutral O atom run is a "
        "closed-shell diagnostic; physical atomic O has an open-shell triplet "
        "ground state."
    ),
    "converged": "OFDFT calculation converged." in stdout,
    "final_grad_norm": float(grad_matches[-1]) if grad_matches else None,
    "total_energy_ha": float(energies.total_energy),
    "total_energy_ev": float(energies.total_energy * hartree_to_ev),
    "electronic_energy_ha": float(energies.electronic_energy),
    "energies_ha": {key: float(value) for key, value in energies.energies_dict.items()},
}
(out / "mofdft_o_atom_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(summary["total_energy_ev"])
PY
)"

"$ROOT_DIR/scripts/build_mofdft_hybrid_from_energy.sh" \
  "$ENERGY_EV" \
  1.0 \
  o_atom_mldft_str25_qm9_closed_shell \
  O \
  "$OUT_DIR/hybrid_o_atom"

echo "Wrote MLDFT atomic-O reference and atomic-O benchmark diagnostic to $OUT_DIR"
