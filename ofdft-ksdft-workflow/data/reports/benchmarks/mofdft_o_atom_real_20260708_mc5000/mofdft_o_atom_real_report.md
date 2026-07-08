# Real MLDFT/M-OFDFT Atomic-O Reference Run

Date: 2026-07-08

This run treats atomic O as its own reference branch. It does not use `1/2 O2`.

The calculation is still a diagnostic rather than a final physical atomic-O
reference because the current `mldft` CLI exposes charge but not spin. Neutral
atomic O has an open-shell triplet ground state, while this run is a
closed-shell MLDFT calculation with charge 0.

## Calculation

| item | value |
| --- | --- |
| code | `mldft` from `structures25` |
| model | `str25_qm9` |
| input | `o_atom.xyz` |
| charge | `0` |
| device | CUDA on remote development machine |
| optimizer | `gradient-descent-torch` |
| max cycles | 5000 |
| convergence tolerance | `1e-4` |
| final gradient norm | `9.979e-05` |
| converged | yes |

The CLI help states that charge is supported and only even electron counts are
supported; no spin option is exposed.

## Energy

| quantity | value |
| --- | ---: |
| O atom total energy | `-75.22094610821165 Ha` |
| O atom total energy | `-2046.866218339195 eV` |
| electronic energy | `-75.22094610821165 Ha` |
| nuclear repulsion | `0.0 Ha` |
| ML kinetic + XC | `66.06738350755185 Ha` |
| Hartree | `37.306363100591255 Ha` |
| nuclear attraction | `-178.59469271635476 Ha` |

Primary output files:

- `o_atom.xyz`
- `o_atom.log`
- `o_atom.pt`
- `o_atom_mldft.stdout`
- `mofdft_o_atom_summary.json`

## Atomic-O Hybrid Benchmark

This candidate uses the same reference convention as the current KSDFT labels:

```text
E_ads^(O atom) = E_WT(Mg slab + O) - E_WT(clean Mg slab) - E_MLDFT(O atom)
```

Benchmark against the 50 KSDFT/PBE Mg(0001)+O adsorption labels:

| metric | value |
| --- | ---: |
| matched structures | 50 |
| adsorption raw MAE | `1561.79 eV` |
| adsorption aligned MAE | `31.5988 eV` |
| adsorption raw RMSE | `1562.31 eV` |
| adsorption aligned RMSE | `40.3647 eV` |
| Spearman | `0.152845` |
| top-1 match | no |

The very large raw MAE is expected. The MLDFT atomic calculation is an
all-electron molecular/atomic calculation, while the Mg slab and adsorbed Mg+O
energies in the current workflow are pseudopotential QE/DFTpy-style energies.
Their absolute energy zeros are not directly compatible.

The aligned MAE and Spearman are unchanged from the previous reference
diagnostics because replacing only the isolated atomic-O reference applies a
constant shift to every adsorption structure.

## Interpretation

This run fixes the reference-species mistake: atomic O is now treated as atomic
O, not as `1/2 O2`.

It also shows that using the absolute all-electron MLDFT atomic-O energy
directly is not a valid production reference for the pseudopotential surface
workflow. For a physically useful atomic-O branch, the next requirement is one
of:

- expose spin in the MLDFT runner and run open-shell atomic O;
- evaluate atomic O in the same pseudopotential Hamiltonian convention as the
  Mg+O workflow;
- use MLDFT atomic O only through a calibrated chemical-potential or residual
  correction built from compatible KSDFT references.
