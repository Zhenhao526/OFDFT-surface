# Pseudopotential-Calibrated MLDFT Atomic-O Reference

Date: 2026-07-08

This run builds the most immediately usable pseudopotential-compatible
atomic-O reference for the current Mg(0001)+O workflow.

Important: this is not a native pseudopotential MLDFT calculation. The current
`mldft` atomic-O calculation is all-electron. Compatibility is introduced by an
explicit energy offset that maps the MLDFT atomic-O total energy onto the
existing QE/PBE pseudopotential atomic-O reference used by the KSDFT adsorption
labels.

## Calibration

The calibrated reference is:

```text
E_O^cal = E_MLDFT(O atom) + delta_O
```

| quantity | value |
| --- | ---: |
| MLDFT atomic-O total energy | `-2046.866218339195 eV` |
| QE/PBE pseudopotential O reference target | `-559.859821812708 eV` |
| fitted `delta_O` | `+1487.006396526487 eV` |
| calibrated atomic-O reference | `-559.8598218127081 eV` |

The calibrated JSONL record is:

- `mofdft_adsorbate_reference.jsonl`

It is tagged as:

```text
reference_id = o_atom_mldft_str25_qm9_pseudo_calibrated_to_qe_o_atom
reference_kind = isolated_adsorbate
formula = O
```

## Hybrid Candidate

The benchmarked candidate uses:

```text
E_ads = E_WT(Mg slab + O) - E_WT(clean Mg slab) - E_O^cal
```

Generated candidate:

- `wt_mg_mofdft_adsorbate.jsonl`

It was built with:

```bash
scripts/build_mofdft_hybrid_from_energy.sh \
  -2046.866218339195 \
  1.0 \
  o_atom_mldft_str25_qm9_pseudo_calibrated_to_qe_o_atom \
  O \
  data/reports/benchmarks/mofdft_o_atom_pseudopotential_calibrated_20260708 \
  1487.006396526487
```

## Benchmark Against KSDFT Atomic-O Labels

| metric | value |
| --- | ---: |
| matched structures | 50 |
| adsorption raw MAE | `77.3621 eV` |
| adsorption aligned MAE | `31.5988 eV` |
| adsorption raw RMSE | `84.9815 eV` |
| adsorption aligned RMSE | `40.3647 eV` |
| adsorption raw mean signed error | `74.7833 eV` |
| Spearman | `0.152845` |
| top-1 match | no |

These values match the earlier KS atomic-O oracle reference diagnostic because
the calibrated MLDFT atomic-O reference is shifted exactly onto the QE/PBE
pseudopotential O reference.

## Interpretation

This is the correct atomic-O species branch for the current labels, unlike the
previous half-O2 diagnostic. It also makes the reference-energy convention
compatible with the pseudopotential surface workflow by explicit calibration.

However, the calibration only changes one constant reference term. It does not
change the adsorbed Mg+O total energies. Therefore the aligned MAE, Spearman
ranking, top-k agreement, and site selectivity remain unchanged.

The remaining accuracy problem is in the adsorbed interface energy evaluated
with the current WT OFDFT setup. The next useful step is to target
`E_WT/MGP/LMGP/MGPA(Mg slab + O)` or train a residual correction after this
atomic-O reference is fixed.

## Limitations

- The underlying MLDFT atomic-O run is closed-shell because the CLI does not
  expose spin; physical atomic O is open-shell triplet.
- The current result is pseudopotential-compatible by calibration, not by a
  native MLDFT pseudopotential Hamiltonian.
- This reference should be used only for the atomic-O adsorption convention,
  not for the O2 chemical-potential branch.
