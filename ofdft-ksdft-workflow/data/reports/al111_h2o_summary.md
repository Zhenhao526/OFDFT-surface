# Workflow Summary: al111_h2o

## Counts

- candidate_structures: 88
- corrected_energy_records: 30
- fast_screen_converged: 88
- fast_screen_records: 88
- ks_manifest_records: 30
- output_missing: 29
- parsed_converged: 1
- parsed_records: 30
- prediction_records: 30
- selected_records: 30

## Status Counts

### selection_reason
- best_in_site_orientation_group: 12
- low_energy_fill: 18

### manifest_status
- input_prepared: 30

### parsed_status
- output_missing: 29
- parsed_converged: 1

## Top Fast-Screen Records

| rank | structure_id | site | orientation | height_angstrom | energy_ev | ks_status |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | c2bb8d36fb6d59b5 | fcc | dipole_down | 2.4 | -0.88091534 |  |
| 1 | b467960d9091ae83 | fcc | dipole_down | 2.4 | -0.88091515 |  |
| 2 | de873c3a9ef3ffe0 | fcc | dipole_down | 2.4 | -0.88091397 |  |
| 3 | 97a8503e75637736 | hcp | dipole_down | 2.4 | -0.86091462 |  |
| 4 | 2b8274a7f1715f83 | fcc | dipole_down | 2.8 | -0.85931534 |  |

## Top Corrected Records

| rank | structure_id | site | orientation | height_angstrom | energy_ev | ks_status |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | c2bb8d36fb6d59b5 | fcc | dipole_down | 2.4 | -217.69108997 | parsed_converged |
| 1 | b467960d9091ae83 | fcc | dipole_down | 2.4 | -217.69108978 | output_missing |
| 2 | de873c3a9ef3ffe0 | fcc | dipole_down | 2.4 | -217.69108860 | output_missing |
| 3 | 97a8503e75637736 | hcp | dipole_down | 2.4 | -217.67108925 | output_missing |
| 4 | 2b8274a7f1715f83 | fcc | dipole_down | 2.8 | -217.66948997 | output_missing |

## Delta Report Excerpt

# Delta-Learning Baseline Report

- Model: `data/processed/models/al111_h2o_delta.json`
- Trainable records: 1 / 30
- Features: 8
- Ridge alpha: 1.0
- Target mean delta energy: -216.81017463 eV
- Train MAE: 0.00000000 eV
- Train RMSE: 0.00000000 eV

Warning: Very small training set; model is only a pipeline sanity check.

## Recommendations

- Increase candidate diversity if this is intended as a production adsorption search.
- Run or attach QE outputs for missing selected jobs; KS labels are the current bottleneck.
- Collect at least 5 parsed_converged KS labels before interpreting the delta model.
