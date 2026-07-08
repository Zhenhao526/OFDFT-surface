# QE Real-Run Report

Date: 2026-07-07

## Environment

- QE executable: `_runtime/q-e-7.4.1/bin/pw.x`
- QE version: `PWSCF v.7.4.1`
- Runtime MPI setting used locally: `OMPI_MCA_btl=self,vader`
- QE environment checks:
  - Production config: `data/reports/qe_env.md`
  - Smoke config: `data/reports/qe_env_smoke.md`

## Pseudopotentials

All current QE inputs use PBE PAW PSL UPF files under `pseudo/`:

- `Al.pbe-n-kjpaw_psl.1.0.0.UPF`
- `Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF`
- `H.pbe-kjpaw_psl.1.0.0.UPF`
- `O.pbe-n-kjpaw_psl.1.0.0.UPF`

## Code Updates

- Resolved QE executable paths to absolute paths before changing into each job directory.
- Added configurable QE input rendering for `calculation`, `control.nstep`, `electrons.conv_thr`, and `electrons.mixing_beta`.
- Wrote `&IONS` only for ionic-dynamics calculations such as `relax`.
- Updated missing-job detection so incomplete `pw.out` files without `JOB DONE.` remain runnable.
- Added local smoke configs:
  - `configs/systems/mg0001_o_smoke.yaml`
  - `configs/calculators/qe_pbe_smoke.yaml`

## Production Attempt

First production candidate attempted:

- Job dir: `data/raw/ksdft/mg0001_o/0001_34ccd72467145eb5`
- Input: 65 atoms, Mg(0001)+O, `relax`, 50/400 Ry, `3 3 1` k-points, PAW, 2D cutoff
- QE successfully read `Mg` and `O` pseudopotentials and entered SCF iteration 1.
- QE estimated max dynamic RAM per process: `> 33.93 GB`.
- The local run was manually interrupted after it remained in SCF iteration 1 for several minutes.
- The partial output is kept at `data/raw/ksdft/mg0001_o/0001_34ccd72467145eb5/pw.out` as a resource diagnostic.

Conclusion: the production input is valid, but this production setting should be run with parallel resources or reduced local settings.

## Completed Smoke Run

Smoke candidate:

- Job dir: `data/raw/ksdft/mg0001_o_smoke/0000_4dd34df24c37a67f`
- Input: 13 atoms, Mg(0001)+O, `scf`, 30/240 Ry, Gamma-only k-point, same PAW UPF set
- Runtime status: `exit_0`
- Wall time recorded by workflow: `15.20 s`
- QE output: `JOB DONE.`
- Parsed status: `parsed_converged`
- Total energy: `-1732.78581339 Ry` / `-23575.75202486 eV`
- Parsed max force: `4.35087845 eV/Ang`

Parsed label:

- `data/processed/labels/mg0001_o_smoke_ks_parsed.jsonl`

## Next Step

Use the smoke route for local regression checks, and use the production manifest on a parallel QE environment for actual labels. For local production experiments, the next controlled reduction should test one change at a time: remove 2D cutoff, lower k-points, or shrink slab size, then compare against the production input before committing it as a scientific setting.
