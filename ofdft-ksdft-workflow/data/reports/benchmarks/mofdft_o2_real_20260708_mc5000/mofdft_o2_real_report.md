# Real MLDFT/M-OFDFT O2 Reference Run

Date: 2026-07-08

This run connects the real `mldft` molecular OFDFT implementation from
`structures25` to the Mg(0001)+O hybrid adsorption workflow.

## Calculation

| item | value |
| --- | --- |
| code | `mldft` from `structures25` |
| model | `str25_qm9` |
| input | `o2.xyz` |
| geometry | O-O = 1.2075 Angstrom |
| device | CUDA on remote development machine |
| optimizer | `gradient-descent-torch` |
| max cycles | 5000 |
| convergence tolerance | `1e-4` |
| final gradient norm | `9.986e-05` |
| converged | yes |

The CLI run is closed-shell because the current `mldft` CLI exposes charge but
not spin. Physical O2 has a triplet ground state, so this result is a first
engineering integration of the molecular OFDFT code path, not a final physical
O2 thermochemical reference.

## Energy

| quantity | value |
| --- | ---: |
| O2 total energy | `-150.1597752262035 Ha` |
| O2 total energy | `-4086.055642290963 eV` |
| 1/2 O2 reference | `-2043.0278211454815 eV` |
| electronic energy | `-178.20726300995506 Ha` |
| nuclear repulsion | `28.047487783751553 Ha` |
| ML kinetic + XC | `132.82687352797956 Ha` |
| Hartree | `100.76437206024401 Ha` |
| nuclear attraction | `-411.7985085981786 Ha` |

Primary output files:

- `o2.xyz`
- `o2.log`
- `o2.pt`
- `o2_mldft.stdout`
- `mofdft_o2_summary.json`

## Hybrid Benchmark

The 1/2 O2 energy was passed to:

```bash
scripts/build_mofdft_hybrid_from_energy.sh \
  -4086.055642290963 \
  0.5 \
  half_o2_mldft_str25_qm9 \
  O2 \
  data/reports/benchmarks/mofdft_o2_real_20260708_mc5000/hybrid_half_o2
```

Benchmark against the 50 KSDFT/PBE Mg(0001)+O adsorption labels:

| metric | value |
| --- | ---: |
| matched structures | 50 |
| adsorption raw MAE | `1557.95 eV` |
| adsorption aligned MAE | `31.5988 eV` |
| Spearman | `0.152845` |
| top-1 match | no |

The aligned MAE is identical to the WT-reference and KS-oracle-reference
diagnostics because replacing the adsorbate reference applies one constant
shift to all adsorption structures.

## Interpretation

This run proves that the real molecular MLDFT/M-OFDFT code path is executable
and can be connected to the local hybrid adsorption workflow.

The raw adsorption MAE is not physically meaningful yet. The molecular MLDFT
calculation is all-electron/PySCF-like, while the Mg slab and adsorbed Mg+O
energies are pseudopotential OFDFT/QE-style energies. These total-energy zeros
are not directly compatible.

Therefore, the current result should be read as a successful software
integration and a diagnostic of reference-energy inconsistency, not as a valid
mixed OFDFT adsorption-energy prediction.

## Next Required Fix

To make M-OFDFT molecular references usable in the Mg surface workflow, one of
the following energy conventions must be introduced:

- train/evaluate molecular M-OFDFT in the same pseudopotential Hamiltonian used
  for the Mg+O workflow;
- convert the molecular all-electron result to a compatible atomization or
  reaction-energy convention rather than inserting its absolute total energy;
- calibrate an oxygen chemical potential offset on shared KSDFT references and
  use M-OFDFT only for molecular deformation or relative corrections;
- expose spin in the MLDFT runner and rerun O2 with the triplet state before any
  physical oxygen chemical-potential analysis.

The immediate engineering next step is to add a calibrated-reference mode:

```text
mu_O = 1/2 E_MOFDFT(O2) + delta_mu_O
```

where `delta_mu_O` is fitted from compatible KSDFT/QE reference calculations
before comparing adsorption energies.
