#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRUCTURES25_DIR="${STRUCTURES25_DIR:-/mnt/afs/home/xiazhenhao/dft/structures25}"
OUT_DIR="${OUT_DIR:-$ROOT_DIR/data/reports/benchmarks/mofdft_o2_real_$(date +%Y%m%d_%H%M%S)}"
MODEL="${MODEL:-str25_qm9}"
DEVICE="${DEVICE:-cuda}"
TRANSFORM_DEVICE="${TRANSFORM_DEVICE:-cpu}"
MAX_CYCLE="${MAX_CYCLE:-5000}"
CONVERGENCE_TOLERANCE="${CONVERGENCE_TOLERANCE:-1e-4}"
LEARNING_RATE="${LEARNING_RATE:-1e-3}"
O2_BOND_ANGSTROM="${O2_BOND_ANGSTROM:-1.2075}"
export MODEL O2_BOND_ANGSTROM

MLDFT_PYTHON="$STRUCTURES25_DIR/.venv/bin/python"
MLDFT_CLI="$STRUCTURES25_DIR/.venv/bin/mldft"
export DFT_DATA="${DFT_DATA:-$STRUCTURES25_DIR/_runtime/data}"
export DFT_MODELS="${DFT_MODELS:-$STRUCTURES25_DIR/_runtime/models}"

mkdir -p "$OUT_DIR"

cat > "$OUT_DIR/o2.xyz" <<EOF
2
O2 closed-shell MLDFT geometry, bond=${O2_BOND_ANGSTROM} Angstrom
O 0.000000 0.000000 0.000000
O 0.000000 0.000000 ${O2_BOND_ANGSTROM}
EOF

(
  cd "$STRUCTURES25_DIR"
  "$MLDFT_CLI" "$OUT_DIR/o2.xyz" \
    --model "$MODEL" \
    --device "$DEVICE" \
    --transform-device "$TRANSFORM_DEVICE" \
    --max-cycle "$MAX_CYCLE" \
    --convergence-tolerance "$CONVERGENCE_TOLERANCE" \
    --learning-rate "$LEARNING_RATE"
) > "$OUT_DIR/o2_mldft.stdout" 2>&1

ENERGY_EV="$("$MLDFT_PYTHON" - "$OUT_DIR" <<'PY'
import json
import os
import pathlib
import re
import sys

import torch

hartree_to_ev = 27.211386245988
out = pathlib.Path(sys.argv[1])
sample = torch.load(out / "o2.pt", map_location="cpu", weights_only=False)
energies = sample.energies
stdout = (out / "o2_mldft.stdout").read_text(errors="ignore")
grad_matches = re.findall(r"grad_norm=([0-9.]+e[+-][0-9]+)", stdout)
summary = {
    "method": "mldft",
    "model": os.environ.get("MODEL", "str25_qm9"),
    "formula": "O2",
    "geometry": f"O-O {os.environ.get('O2_BOND_ANGSTROM', '1.2075')} Angstrom",
    "spin_note": (
        "mldft CLI run is closed-shell/singlet because spin is not exposed by the CLI; "
        "O2 physical ground state is triplet."
    ),
    "converged": "OFDFT calculation converged." in stdout,
    "final_grad_norm": float(grad_matches[-1]) if grad_matches else None,
    "total_energy_ha": float(energies.total_energy),
    "total_energy_ev": float(energies.total_energy * hartree_to_ev),
    "half_o2_energy_ev": float(energies.total_energy * hartree_to_ev * 0.5),
    "electronic_energy_ha": float(energies.electronic_energy),
    "energies_ha": {key: float(value) for key, value in energies.energies_dict.items()},
}
(out / "mofdft_o2_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(summary["total_energy_ev"])
PY
)"

"$ROOT_DIR/scripts/build_mofdft_hybrid_from_energy.sh" \
  "$ENERGY_EV" \
  0.5 \
  half_o2_mldft_str25_qm9 \
  O2 \
  "$OUT_DIR/hybrid_half_o2"

echo "Wrote MLDFT O2 reference and hybrid benchmark to $OUT_DIR"
