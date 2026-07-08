# Calibrated MLDFT/M-OFDFT O2 Reference Benchmark

Date: 2026-07-08

This report continues the real `mldft` O2 run by adding the calibrated
reference-energy mode needed for the current Mg(0001)+O adsorption workflow.

The key issue is energy convention compatibility. The `mldft` O2 calculation is
an all-electron molecular calculation, while the Mg slab and Mg+O adsorbed
energies in the current benchmark are QE/DFTpy pseudopotential-style energies.
Their absolute total-energy zeros cannot be mixed directly.

## Calibration

The calibrated oxygen chemical potential is:

```text
mu_O = 1/2 E_MLDFT(O2) + delta_mu_O
```

where `delta_mu_O` shifts the all-electron half-O2 value onto the current
QE/PBE isolated-O-atom reference convention used by the existing adsorption
labels.

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

The benchmarked hybrid candidate uses:

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

## Benchmark Against KSDFT Adsorption Labels

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
calibrated MLDFT half-O2 reference has been shifted exactly onto the same QE O
atom reference energy.

## Interpretation

The calibrated-reference mode solves the immediate software integration
problem: a real MLDFT molecular energy can now be passed through the hybrid
adsorption workflow with an explicit convention shift.

It does not solve the main accuracy problem. Replacing only the isolated oxygen
reference applies a constant shift to every adsorption structure. Therefore it
can reduce the absolute raw adsorption-energy offset, but it cannot improve the
relative ranking, Spearman correlation, top-k agreement, or site selectivity.

The remaining error is dominated by the adsorbed Mg+O total energy evaluated
with the current WT OFDFT setup.

## Next Research Step

The next technically meaningful step should target the adsorbed interface
energy, not only the isolated molecule reference. The most useful branches are:

- run additional KEDFs such as LMGP/MGP/MGPA/HC-style candidates on the same
  adsorbed Mg+O structures and compare adsorption ranking;
- add a delta model on top of calibrated OFDFT adsorption energies and measure
  whether the residual correction improves aligned MAE and Spearman;
- expose spin in the `mldft` runner and rerun O2 as triplet before using any
  physical O2 chemical-potential convention;
- build or identify a pseudopotential-compatible molecular M-OFDFT path so
  absolute molecular and slab energies share the same Hamiltonian convention.
