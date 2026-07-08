# Reference-Mismatch Diagnostic: MLDFT/M-OFDFT O2 vs Atomic-O Labels

Date: 2026-07-08

Correction: this directory is retained only as a software/reference-mismatch
diagnostic. It must not be used as a physical adsorption benchmark.

The current Mg(0001)+O KSDFT labels use an isolated atomic-O reference. Atomic O
cannot be treated as `1/2 O2` in this benchmark. The O atom and O2 molecule must
be handled as separate reference conventions.

This report continues the real `mldft` O2 run by showing what happens if the
half-O2 energy is forced onto the current atomic-O reference convention.

The key issue is energy convention compatibility. The `mldft` O2 calculation is
an all-electron molecular calculation, while the Mg slab and Mg+O adsorbed
energies in the current benchmark are QE/DFTpy pseudopotential-style energies.
Their absolute total-energy zeros cannot be mixed directly.

## Diagnostic Shift

The diagnostic shift used here is:

```text
mu_O = 1/2 E_MLDFT(O2) + delta_mu_O
```

where `delta_mu_O` shifts the all-electron half-O2 value onto the current
QE/PBE isolated-O-atom reference convention used by the existing adsorption
labels. This is a bookkeeping test, not a physical identification of atomic O
with half an O2 molecule.

| quantity | value |
| --- | ---: |
| MLDFT O2 total energy | `-4086.055642290963 eV` |
| 1/2 MLDFT O2 | `-2043.0278211454815 eV` |
| QE/PBE O atom reference target | `-559.859821812708 eV` |
| fitted `delta_mu_O` | `+1483.1679993327735 eV` |
| calibrated O reference | `-559.8598218127081 eV` |

The reference JSONL record is:

- `mofdft_adsorbate_reference.jsonl`

This is an engineering calibration against the current pseudopotential
reference convention. It is not an independent physical O2 adsorption
benchmark.

## Hybrid Candidate

The diagnostic hybrid candidate uses:

```text
E_ads = E_WT(Mg slab + O) - E_WT(clean Mg slab) - mu_O_calibrated
```

The generated candidate file is:

- `wt_mg_mofdft_adsorbate.jsonl`

It was built with:

```bash
scripts/build_mofdft_hybrid_from_energy.sh \
  -4086.055642290963 \
  0.5 \
  half_o2_mldft_str25_qm9_calibrated_to_qe_o_atom \
  O2 \
  data/reports/benchmarks/mofdft_o2_calibrated_reference_20260708 \
  1483.1679993327735
```

## Invalid Cross-Convention Comparison

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

These values match the earlier `wt_slab_ks_o_oracle` diagnostic because the
half-O2 number was shifted exactly onto the same QE O atom reference energy.
They should not be interpreted as an O2-referenced adsorption benchmark.

## Interpretation

The explicit energy-shift mode is still useful for software integration tests,
but this particular O2-to-O-atom shift is not a valid physical treatment of
oxygen.

Replacing only the oxygen reference applies a constant shift to every adsorption
structure. Therefore it cannot improve the relative ranking, Spearman
correlation, top-k agreement, or site selectivity.

The remaining error is dominated by the adsorbed Mg+O total energy evaluated
with the current WT OFDFT setup.

## Corrected Research Step

The corrected workflow must keep two branches separate:

- Atomic-O reference branch: compare against the existing
  `mg0001_o_pilot_all50_ks_adsorption.jsonl` labels, and supply an atomic-O
  reference from a method that can represent the O atom consistently.
- O2 chemical-potential branch: compute or build KSDFT truth with the same
  `1/2 E(O2)` reference before comparing adsorption energies.

After the reference convention is correct, the next technically meaningful step
should target the adsorbed interface energy. The most useful branches are:

- run additional KEDFs such as LMGP/MGP/MGPA/HC-style candidates on the same
  adsorbed Mg+O structures and compare adsorption ranking;
- add a delta model on top of calibrated OFDFT adsorption energies and measure
  whether the residual correction improves aligned MAE and Spearman;
- expose spin in the `mldft` runner and rerun O2 as triplet before using any
  physical O2 chemical-potential convention;
- build or identify a pseudopotential-compatible molecular M-OFDFT path so
  absolute molecular and slab energies share the same Hamiltonian convention.
