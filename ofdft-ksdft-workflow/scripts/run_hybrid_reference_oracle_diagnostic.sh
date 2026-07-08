#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
export PYTHONPATH="${PYTHONPATH:-$ROOT_DIR/src}"

cd "$ROOT_DIR"

OUT_DIR="data/reports/benchmarks/hybrid_reference_oracle_diagnostic_20260708"
ADSORBED="data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl"
WT_REFS="data/processed/screens/mg0001_o_pilot_references_dftpy_pbe_wt_atomic_m100.jsonl"
KS_REFS="data/processed/labels/mg0001_o_pilot_references_scf_ks_parsed.jsonl"
TRUTH="data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl"

mkdir -p "$OUT_DIR"

"$PYTHON_BIN" -m ofks.workflows.build_hybrid_adsorption \
  --adsorbed "$ADSORBED" \
  --slab-reference "$WT_REFS" \
  --adsorbate-reference "$WT_REFS" \
  --candidate-name wt_refs \
  --backend hybrid_reference_diagnostic \
  --adsorbed-source wt_adsorbed \
  --slab-source wt_mg_slab \
  --adsorbate-source wt_o_atom \
  --out "$OUT_DIR/wt_refs.jsonl"

"$PYTHON_BIN" -m ofks.workflows.build_hybrid_adsorption \
  --adsorbed "$ADSORBED" \
  --slab-reference "$WT_REFS" \
  --adsorbate-reference "$KS_REFS" \
  --candidate-name wt_slab_ks_o_oracle \
  --backend hybrid_reference_diagnostic \
  --adsorbed-source wt_adsorbed \
  --slab-source wt_mg_slab \
  --adsorbate-source ks_o_oracle \
  --adsorbate-energy-key ks_total_energy_ev \
  --out "$OUT_DIR/wt_slab_ks_o_oracle.jsonl"

"$PYTHON_BIN" -m ofks.workflows.build_hybrid_adsorption \
  --adsorbed "$ADSORBED" \
  --slab-reference "$KS_REFS" \
  --adsorbate-reference "$WT_REFS" \
  --candidate-name ks_slab_wt_o \
  --backend hybrid_reference_diagnostic \
  --adsorbed-source wt_adsorbed \
  --slab-source ks_mg_slab_oracle \
  --adsorbate-source wt_o_atom \
  --slab-energy-key ks_total_energy_ev \
  --out "$OUT_DIR/ks_slab_wt_o.jsonl"

"$PYTHON_BIN" -m ofks.workflows.build_hybrid_adsorption \
  --adsorbed "$ADSORBED" \
  --slab-reference "$KS_REFS" \
  --adsorbate-reference "$KS_REFS" \
  --candidate-name ks_refs_oracle \
  --backend hybrid_reference_diagnostic \
  --adsorbed-source wt_adsorbed \
  --slab-source ks_mg_slab_oracle \
  --adsorbate-source ks_o_oracle \
  --slab-energy-key ks_total_energy_ev \
  --adsorbate-energy-key ks_total_energy_ev \
  --out "$OUT_DIR/ks_refs_oracle.jsonl"

"$PYTHON_BIN" -m ofks.workflows.benchmark_algorithms \
  --truth "$TRUTH" \
  --candidate "wt_refs=$OUT_DIR/wt_refs.jsonl" \
  --candidate "wt_slab_ks_o_oracle=$OUT_DIR/wt_slab_ks_o_oracle.jsonl" \
  --candidate "ks_slab_wt_o=$OUT_DIR/ks_slab_wt_o.jsonl" \
  --candidate "ks_refs_oracle=$OUT_DIR/ks_refs_oracle.jsonl" \
  --out-json "$OUT_DIR/benchmark.json" \
  --out-md "$OUT_DIR/benchmark.md" \
  --out-csv "$OUT_DIR/benchmark.csv"

echo "Wrote hybrid reference oracle diagnostic to $OUT_DIR"
