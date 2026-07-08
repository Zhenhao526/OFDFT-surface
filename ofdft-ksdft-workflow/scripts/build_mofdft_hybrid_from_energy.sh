#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/build_mofdft_hybrid_from_energy.sh ENERGY_EV ENERGY_SCALE REFERENCE_ID FORMULA OUT_DIR

Examples:
  # O atom reference from external M-OFDFT:
  scripts/build_mofdft_hybrid_from_energy.sh -560.0 1.0 o_atom_mofdft O data/reports/benchmarks/mofdft_o_atom_hybrid

  # Half-O2 reference from external M-OFDFT:
  scripts/build_mofdft_hybrid_from_energy.sh -1120.0 0.5 half_o2_mofdft O2 data/reports/benchmarks/mofdft_half_o2_hybrid

The script keeps WT for the Mg slab and WT for the adsorbed Mg+O structures,
then replaces only the adsorbate reference with the supplied external energy.
EOF
}

if [[ $# -ne 5 ]]; then
  usage
  exit 2
fi

ENERGY_EV="$1"
ENERGY_SCALE="$2"
REFERENCE_ID="$3"
FORMULA="$4"
OUT_DIR="$5"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
export PYTHONPATH="${PYTHONPATH:-$ROOT_DIR/src}"

cd "$ROOT_DIR"

ADSORBED="data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl"
WT_REFS="data/processed/screens/mg0001_o_pilot_references_dftpy_pbe_wt_atomic_m100.jsonl"
TRUTH="data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl"
REFERENCE_JSONL="$OUT_DIR/mofdft_adsorbate_reference.jsonl"
HYBRID_JSONL="$OUT_DIR/wt_mg_mofdft_adsorbate.jsonl"

mkdir -p "$OUT_DIR"

"$PYTHON_BIN" -m ofks.workflows.build_reference_energy \
  --energy-ev "$ENERGY_EV" \
  --energy-scale "$ENERGY_SCALE" \
  --reference-id "$REFERENCE_ID" \
  --adsorbate O \
  --formula "$FORMULA" \
  --backend mofdft \
  --candidate-name mofdft_adsorbate_reference \
  --reference-convention "${FORMULA}_scale_$ENERGY_SCALE" \
  --out "$REFERENCE_JSONL"

"$PYTHON_BIN" -m ofks.workflows.build_hybrid_adsorption \
  --adsorbed "$ADSORBED" \
  --slab-reference "$WT_REFS" \
  --adsorbate-reference "$REFERENCE_JSONL" \
  --candidate-name wt_mg_mofdft_adsorbate \
  --backend hybrid_ofdft \
  --adsorbed-source wt_adsorbed \
  --slab-source wt_mg_slab \
  --adsorbate-source mofdft_adsorbate \
  --adsorbate-reference-id "$REFERENCE_ID" \
  --out "$HYBRID_JSONL"

"$PYTHON_BIN" -m ofks.workflows.benchmark_algorithms \
  --truth "$TRUTH" \
  --candidate "wt_mg_mofdft_adsorbate=$HYBRID_JSONL" \
  --out-json "$OUT_DIR/benchmark.json" \
  --out-md "$OUT_DIR/benchmark.md" \
  --out-csv "$OUT_DIR/benchmark.csv"

echo "Wrote M-OFDFT hybrid candidate and benchmark to $OUT_DIR"
