# OFDFT-Assisted KSDFT Surface Adsorption Workflow: Code Execution Taskbook

## 1. Project Goal

Build a reproducible code workflow for simple-metal surface adsorption studies:

```text
candidate generation -> fast OFDFT/ML screening -> KSDFT validation -> delta-learning correction -> active learning loop
```

The first-stage goal is not to replace KSDFT with a fully self-consistent OFDFT/M-OFDFT hybrid. The goal is to reduce the number of expensive KSDFT relaxations while preserving reliable low-energy adsorption structures, adsorption-site ranking, and adsorption energies.

Target first demonstration:

- `H2O/Al(111)` for weak adsorption and dipole-sensitive adsorption.
- `O/Mg(0001)` for stronger adsorption and early oxidation behavior.
- Optional easier warm-up: `H/Al(111)` and `H/Mg(0001)`.

## 2. Scope

### In Scope

- Structure generation for simple-metal slabs and adsorbate placements.
- OFDFT-based or ML-based fast relaxation/screening.
- KSDFT reference calculation orchestration.
- Parsing, normalization, and comparison of OFDFT/KSDFT results.
- Delta-learning model for energy and force correction.
- Active learning loop for selecting new KSDFT calculations.
- Benchmark reports and reproducible examples.

### Out of Scope for Phase 1

- Fully self-consistent density-level coupling between M-OFDFT and metal OFDFT.
- Production-level electrochemical constant-potential simulations.
- Transition-metal surfaces with d-electron chemistry.
- Strongly correlated or magnetic surfaces.
- General-purpose universal adsorption model.

## 3. Recommended Software Stack

### Core

- Python 3.10+
- ASE for structures, constraints, calculators, trajectories, and file I/O.
- NumPy/SciPy for numerical utilities.
- pandas/pyarrow for tabular datasets.
- pydantic or dataclasses for typed metadata.
- pytest for tests.

### DFT / OFDFT Backends

- DFTpy as the first OFDFT backend, because it is Python-friendly and ASE-compatible.
- PROFESS as optional OFDFT backend if available.
- Quantum ESPRESSO, VASP, or GPAW as KSDFT backend.
- Initial recommendation: use Quantum ESPRESSO or GPAW for open-source reproducibility.

### ML Components

- scikit-learn for baseline kernel/ridge models.
- PyTorch for force-aware delta-learning.
- Optional: MACE, NequIP, Allegro, or OC models for MLFF-based screening.

## 4. Proposed Repository Structure

```text
ofdft-ksdft-workflow/
  README.md
  pyproject.toml
  configs/
    systems/
      al111_h2o.yaml
      mg0001_o.yaml
    calculators/
      qe_pbe.yaml
      dftpy_al.yaml
      dftpy_mg.yaml
    workflows/
      screening.yaml
      active_learning.yaml
  data/
    raw/
      ksdft/
      ofdft/
      mlff/
    processed/
      structures/
      labels/
      splits/
    reports/
  src/
    ofks/
      __init__.py
      structures/
        slabs.py
        adsorbates.py
        placements.py
        constraints.py
      calculators/
        base.py
        dftpy_runner.py
        qe_runner.py
        vasp_runner.py
        mlff_runner.py
      workflows/
        generate_candidates.py
        run_fast_screen.py
        run_ks_validation.py
        train_delta.py
        active_select.py
        summarize.py
      parsers/
        qe.py
        dftpy.py
        generic.py
      data/
        schema.py
        dataset.py
        featurize.py
      models/
        delta_energy.py
        delta_force.py
        uncertainty.py
      metrics/
        adsorption.py
        ranking.py
        geometry.py
      utils/
        hashing.py
        logging.py
        units.py
  scripts/
    make_al111_h2o_candidates.py
    make_mg0001_o_candidates.py
  tests/
    test_structure_generation.py
    test_adsorption_energy.py
    test_parsers.py
    test_delta_model.py
  examples/
    al111_h2o/
    mg0001_o/
```

## 5. Data Model

Every structure should have a stable identifier and complete provenance. Use a metadata sidecar file for each structure or store equivalent fields in a parquet/JSONL dataset.

### Structure Record

```yaml
structure_id: al111_h2o_000123
parent_id: al111_clean_4x4x4
system:
  surface: Al(111)
  adsorbate: H2O
  coverage: 0.0625
  slab_size: [4, 4, 4]
  vacuum_angstrom: 18.0
  fixed_layers: 2
placement:
  site: top
  orientation: dipole_down
  height_angstrom: 2.6
  lateral_shift: [0.0, 0.0]
calculation:
  backend: qe
  xc: PBE
  dispersion: vdW-DF2
  kpoints: [3, 3, 1]
  smearing: cold
  degauss_ry: 0.02
  ecutwfc_ry: 50
  ecutrho_ry: 400
labels:
  total_energy_ev: null
  adsorption_energy_ev: null
  max_force_ev_per_ang: null
  converged: false
files:
  input: path/to/input.in
  output: path/to/output.out
  trajectory: path/to/traj.extxyz
```

### Required Labels

- `E_slab`
- `E_adsorbate`
- `E_slab_adsorbate`
- `E_ads = E_slab_adsorbate - E_slab - E_adsorbate`
- relaxed geometry
- forces
- convergence status
- final adsorption site classification
- anomaly flag: desorption, dissociation, surface reconstruction, adsorbate migration

## 6. Workflow Modules

### Module A: Structure Generation

Purpose: generate clean slabs, adsorbates, and adsorption candidates.

Required functions:

- `build_slab(element, miller, size, layers, vacuum, fixed_layers)`
- `build_adsorbate(name)`
- `enumerate_sites(slab, site_types)`
- `place_adsorbate(slab, adsorbate, site, height, orientation)`
- `deduplicate_structures(structures, tolerance)`

CLI target:

```bash
ofks-generate \
  --system configs/systems/al111_h2o.yaml \
  --out data/processed/structures/al111_h2o_candidates.extxyz
```

Definition of Done:

- Can generate clean `Al(111)` and `Mg(0001)` slabs.
- Can generate top, bridge, fcc, hcp placements.
- Can generate multiple molecular orientations for H2O.
- Has tests for atom counts, cell vectors, vacuum, fixed-layer tags, and adsorbate placement height.

### Module B: Fast Screening

Purpose: relax or score candidate structures using OFDFT/MLFF/cheap surrogate.

Backends:

- DFTpy for clean metal and metal-dominated structures.
- MLFF or simple interaction model for adsorbate placement pre-screening.
- Optional M-OFDFT for isolated molecular energy or molecular deformation penalty.

CLI target:

```bash
ofks-fast-screen \
  --structures data/processed/structures/al111_h2o_candidates.extxyz \
  --calculator configs/calculators/dftpy_al.yaml \
  --out data/raw/ofdft/al111_h2o_screen.jsonl
```

Definition of Done:

- Runs fast calculations for at least 100 candidate structures.
- Stores energies, forces if available, runtime, and convergence status.
- Produces ranked candidates.
- Does not overwrite existing completed calculations unless `--force` is set.

### Module C: KSDFT Validation

Purpose: run high-quality reference calculations on selected candidates.

CLI target:

```bash
ofks-ks-validate \
  --selected data/processed/splits/al111_h2o_topk.jsonl \
  --calculator configs/calculators/qe_pbe.yaml \
  --out data/raw/ksdft/al111_h2o/
```

Definition of Done:

- Can write QE input files from ASE structures.
- Can parse final energy, forces, relaxed coordinates, and convergence state.
- Can calculate adsorption energies with consistent reference energies.
- Can resume incomplete calculation folders.

### Module D: Delta-Learning

Purpose: learn corrections from fast results to KSDFT labels.

Targets:

```text
Delta E = E_KSDFT - E_fast
Delta F = F_KSDFT - F_fast
```

Baseline models:

- Ridge regression on handcrafted features.
- Kernel ridge regression on SOAP-like descriptors.
- Small equivariant neural network if enough data is available.

CLI target:

```bash
ofks-train-delta \
  --dataset data/processed/labels/al111_h2o_train.parquet \
  --model-out data/processed/models/al111_h2o_delta.pt \
  --report data/reports/al111_h2o_delta_metrics.md
```

Definition of Done:

- Train/validation/test split is reproducible.
- Reports energy MAE, force RMSE, and ranking metrics.
- Saves model, config, scaler, and training metadata.
- Includes baseline model before complex neural model.

### Module E: Active Learning

Purpose: select the next batch of KSDFT calculations.

Selection criteria:

- Low predicted corrected energy.
- High uncertainty.
- Disagreement between OFDFT ranking and delta-corrected ranking.
- Structurally diverse candidates.
- Near-degenerate adsorption sites.

CLI target:

```bash
ofks-active-select \
  --pool data/raw/ofdft/al111_h2o_screen.jsonl \
  --model data/processed/models/al111_h2o_delta.pt \
  --budget 32 \
  --out data/processed/splits/al111_h2o_next_ks.jsonl
```

Definition of Done:

- Can select a batch with no duplicate structures.
- Produces a human-readable selection report.
- Tracks why each structure was selected.

### Module F: Benchmark and Report

Purpose: compare direct KSDFT enumeration with the accelerated workflow.

Metrics:

- adsorption energy MAE
- force RMSE
- top-1/top-3 low-energy hit rate
- Spearman rank correlation
- geometry RMSD after KSDFT relaxation
- adsorption height error
- final site classification accuracy
- number of KSDFT relaxations saved
- wall-time speedup estimate

CLI target:

```bash
ofks-summarize \
  --system al111_h2o \
  --labels data/processed/labels/al111_h2o_all.parquet \
  --out data/reports/al111_h2o_summary.md
```

Definition of Done:

- Produces tables and plots for each metric.
- Separates weak adsorption, chemisorption, and anomalous structures.
- Gives clear recommendation on whether the workflow is useful for the tested system.

## 7. Milestones

### M0: Environment and Skeleton

Tasks:

- Create Python package skeleton.
- Add config loading.
- Add logging and deterministic structure hashing.
- Add pytest setup.

Acceptance:

- `pytest` passes.
- `ofks --help` or equivalent CLI works.

### M1: Clean Metal Benchmark

Systems:

- bulk Al
- bulk Mg
- `Al(111)`
- `Mg(0001)`

Tasks:

- Generate structures.
- Run KSDFT and OFDFT.
- Compare lattice constant, surface energy, work function if available, and layer relaxation.

Acceptance:

- A benchmark table is generated.
- OFDFT settings are fixed for the first adsorption tests.

### M2: Candidate Generation

Systems:

- `H/Al(111)`
- `H2O/Al(111)`
- `O/Mg(0001)`

Tasks:

- Enumerate adsorption sites.
- Generate molecular orientations.
- Deduplicate candidate structures.

Acceptance:

- At least 100 candidates for `H2O/Al(111)`.
- At least 50 candidates for `O/Mg(0001)`.

### M3: Fast Screening Pipeline

Tasks:

- Run fast scores/relaxations.
- Rank candidates.
- Select top-k and diverse structures.

Acceptance:

- Pipeline can run end to end on one example.
- Runtime and failure cases are logged.

### M4: KSDFT Validation Pipeline

Tasks:

- Generate QE/GPAW/VASP inputs.
- Parse outputs.
- Compute adsorption energies.

Acceptance:

- At least 30 validated KSDFT calculations for one target system.
- Output dataset is usable by delta-learning module.

### M5: Delta-Learning Prototype

Tasks:

- Train baseline correction model.
- Evaluate top-k hit rate and adsorption-energy error.
- Select next KSDFT batch.

Acceptance:

- Corrected ranking improves over raw fast ranking.
- Report includes uncertainty or disagreement-based next-batch selection.

### M6: Demonstration Case

Tasks:

- Complete active learning loop for one target system.
- Compare against direct KSDFT enumeration on a small reference set.

Acceptance:

- Demonstrate at least 50 percent reduction in KSDFT relaxations for finding the same low-energy basin.
- Produce final reproducible report.

## 8. Initial Benchmark Systems

### Tier 0: Method Sanity

- bulk Al
- bulk Mg
- clean `Al(111)`
- clean `Mg(0001)`

Purpose:

- Validate OFDFT KEDF and local pseudopotential choices.
- Establish surface model settings before adsorption.

### Tier 1: Simple Adsorption

- `H/Al(111)`
- `H/Mg(0001)`
- `H2/Al(111)`

Purpose:

- Test adsorption-site ranking with simple adsorbates.
- Avoid complex molecular orientation in the first debugging round.

### Tier 2: Corrosion-Relevant Adsorption

- `H2O/Al(111)`
- `O/Mg(0001)`
- `O/Al(111)`
- `OH/Al(111)`

Purpose:

- Enter realistic surface chemistry while keeping metals simple.
- Test weak adsorption, strong adsorption, charge transfer, and surface distortion.

### Tier 3: Larger and More Realistic Systems

- defective `Al(111)` with vacancy or step
- `H2O + OH` coadsorption on `Al(111)`
- explicit water layer on `Al(111)`
- oxygen incorporation/subsurface O on `Mg(0001)`

Purpose:

- Test whether the workflow scales to more realistic corrosion/interface questions.

## 9. Configuration Conventions

### System Config Example

```yaml
name: al111_h2o
surface:
  element: Al
  miller: [1, 1, 1]
  size: [4, 4, 4]
  vacuum_angstrom: 18.0
  fixed_layers: 2
adsorbate:
  name: H2O
  orientations:
    - dipole_down
    - dipole_up
    - flat
  heights_angstrom: [2.0, 2.4, 2.8, 3.2]
placement:
  sites: [top, bridge, fcc, hcp]
  lateral_jitter_angstrom: 0.15
deduplication:
  rmsd_tolerance_angstrom: 0.15
references:
  slab_id: al111_clean_4x4x4
  adsorbate_id: h2o_gas
```

### Calculator Config Example

```yaml
backend: qe
xc: PBE
dispersion: vdW-DF2
pseudopotentials:
  Al: Al.pbe-n-kjpaw_psl.1.0.0.UPF
  H: H.pbe-kjpaw_psl.1.0.0.UPF
  O: O.pbe-n-kjpaw_psl.1.0.0.UPF
ecutwfc_ry: 50
ecutrho_ry: 400
kpoints: [3, 3, 1]
smearing:
  type: cold
  degauss_ry: 0.02
relax:
  fmax_ev_per_ang: 0.05
  max_steps: 120
dipole_correction: true
```

## 10. Testing Plan

### Unit Tests

- slab atom count and cell shape
- fixed-layer constraints
- adsorption-site placement
- adsorption energy formula
- parser robustness on sample outputs
- stable structure hashing

### Integration Tests

- generate 10 candidates for `H/Al(111)`
- run fake calculator
- parse fake outputs
- train a tiny delta model
- produce a summary report

### Scientific Regression Tests

- clean Al bulk lattice constant remains within a configured tolerance.
- clean Mg bulk lattice constant remains within a configured tolerance.
- adsorption energy formula is invariant to record order.
- top-k selection is deterministic for a fixed seed.

## 11. Success Metrics

Minimum target for the first demonstration:

- top-3 low-energy basin hit rate: at least 80 percent
- adsorption energy MAE after correction: 0.1 to 0.2 eV
- force RMSE after correction: 0.05 to 0.15 eV/Angstrom
- KSDFT relaxation count reduction: at least 50 percent
- reproducible workflow from config to final report

Stretch target:

- active learning loop reaches stable ranking within 3 rounds
- corrected model transfers from `H/Al(111)` to `H2O/Al(111)` after small fine-tuning set
- model remains useful on larger slab than used in initial training

## 12. Key Risks and Mitigations

### Risk: OFDFT Does Not Describe Adsorbate Chemistry Well

Mitigation:

- Use OFDFT mainly for metal-dominated structures and pre-equilibration.
- Keep KSDFT validation in the loop.
- Use delta-learning to correct adsorption-specific errors.

### Risk: Local Pseudopotentials Are Not Transferable

Mitigation:

- Start with Al and Mg.
- Benchmark bulk and clean surfaces before adsorption.
- Keep pseudopotential choice fixed once accepted.

### Risk: Fast Ranking Misses the Correct Low-Energy Basin

Mitigation:

- Use top-k plus diversity selection instead of top-1 selection.
- Add uncertainty and disagreement criteria.
- Include randomly sampled candidates in early active learning rounds.

### Risk: Strong Chemisorption Causes Large Errors

Mitigation:

- Start with weak adsorption and simple atomic adsorption.
- Treat O/OH chemisorption as Tier 2.
- Expand KSDFT training data around reactive geometries.

### Risk: Workflow Becomes Backend-Specific

Mitigation:

- Define calculator adapter interfaces.
- Keep structure, metadata, labels, and reports backend-neutral.
- Store raw outputs for reproducibility.

## 13. Deliverables

### Code Deliverables

- Python package with CLI commands.
- Config-driven workflow examples.
- Calculator adapters for at least one OFDFT backend and one KSDFT backend.
- Dataset parser and schema.
- Baseline delta-learning model.
- Active selection module.
- Automated benchmark report generator.

### Data Deliverables

- Clean metal benchmark dataset.
- Adsorption candidate dataset for one target system.
- KSDFT validation dataset.
- Delta-learning train/validation/test split.

### Report Deliverables

- OFDFT vs KSDFT clean metal benchmark.
- Adsorption screening report.
- Delta-learning model report.
- Final demonstration report with speedup estimate and scientific reliability assessment.

## 14. First Four-Week Execution Plan

### Week 1

- Create repository skeleton.
- Implement config loader.
- Implement slab and adsorbate builders.
- Add tests for `Al(111)` and `Mg(0001)` generation.

### Week 2

- Implement adsorption-site enumeration.
- Generate `H/Al(111)` and `H2O/Al(111)` candidates.
- Implement structure hashing and deduplication.
- Create first example configs.

### Week 3

- Implement fake calculator interface for integration tests.
- Implement QE input writer and parser stub.
- Implement DFTpy adapter stub.
- Define result JSONL/parquet schema.

### Week 4

- Run first small KSDFT/OFDFT calculation manually or through adapters.
- Parse outputs into common schema.
- Implement adsorption energy computation.
- Generate first benchmark report template.

## 15. Recommended First PRs

1. `repo-skeleton-and-configs`
2. `structure-generation-al-mg-slabs`
3. `adsorbate-placement-and-deduplication`
4. `calculator-adapter-interface`
5. `qe-input-parser-minimal`
6. `dftpy-runner-minimal`
7. `dataset-schema-and-adsorption-energy`
8. `fast-screening-cli`
9. `delta-learning-baseline`
10. `active-selection-and-report`

## 16. Phase-1 Done Definition

Phase 1 is complete when the following command sequence works for one target system:

```bash
ofks-generate --system configs/systems/al111_h2o.yaml --out data/processed/structures/al111_h2o.extxyz
ofks-fast-screen --structures data/processed/structures/al111_h2o.extxyz --calculator configs/calculators/dftpy_al.yaml --out data/raw/ofdft/al111_h2o_screen.jsonl
ofks-active-select --pool data/raw/ofdft/al111_h2o_screen.jsonl --budget 30 --out data/processed/splits/al111_h2o_ks_batch.jsonl
ofks-ks-validate --selected data/processed/splits/al111_h2o_ks_batch.jsonl --calculator configs/calculators/qe_pbe.yaml --out data/raw/ksdft/al111_h2o/
ofks-train-delta --dataset data/processed/labels/al111_h2o_train.parquet --model-out data/processed/models/al111_h2o_delta.pt --report data/reports/al111_h2o_delta.md
ofks-summarize --system al111_h2o --labels data/processed/labels/al111_h2o_all.parquet --out data/reports/al111_h2o_summary.md
```

The final summary must state:

- how many candidate structures were generated
- how many fast calculations succeeded
- how many KSDFT calculations were needed
- whether the low-energy KSDFT basin was found
- estimated KSDFT calculation savings
- whether the method is ready for the next target system
