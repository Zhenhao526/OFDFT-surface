# Workflow Summary: mg0001_o

## Counts

- candidate_structures: 12
- corrected_energy_records: 8
- fast_screen_converged: 12
- fast_screen_records: 12
- ks_manifest_records: 8
- output_missing: 7
- parsed_converged: 1
- parsed_records: 8
- prediction_records: 8
- selected_records: 8

## Status Counts

### selection_reason
- best_in_site_orientation_group: 4
- low_energy_fill: 4

### manifest_status
- input_prepared: 8

### parsed_status
- output_missing: 7
- parsed_converged: 1

## Top Fast-Screen Records

| rank | structure_id | site | orientation | height_angstrom | energy_ev | ks_status |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | f34254a14fb24f63 | fcc | atom | 2.4 | -0.77482985 |  |
| 1 | 34ccd72467145eb5 | hcp | atom | 2.4 | -0.75482996 |  |
| 2 | c91a54a9cfb138cd | bridge | atom | 2.4 | -0.74482873 |  |
| 3 | 8b1acf85e5e7a650 | fcc | atom | 2.0 | -0.73882985 |  |
| 4 | 8b8acc0f2a107268 | hcp | atom | 2.0 | -0.71882996 |  |

## Top Corrected Records

| rank | structure_id | site | orientation | height_angstrom | energy_ev | ks_status |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | f34254a14fb24f63 | fcc | atom | 2.4 | -217.69108997 | parsed_converged |
| 1 | 34ccd72467145eb5 | hcp | atom | 2.4 | -217.67109008 | output_missing |
| 2 | c91a54a9cfb138cd | bridge | atom | 2.4 | -217.66108884 | output_missing |
| 3 | 8b1acf85e5e7a650 | fcc | atom | 2.0 | -217.65508997 | output_missing |
| 4 | 8b8acc0f2a107268 | hcp | atom | 2.0 | -217.63509008 | output_missing |

## Delta Report Excerpt

# Delta-Learning Baseline Report

- Model: `data/processed/models/mg0001_o_delta.json`
- Trainable records: 1 / 8
- Features: 8
- Ridge alpha: 1.0
- Target mean delta energy: -216.91626011 eV
- Train MAE: 0.00000000 eV
- Train RMSE: 0.00000000 eV

Warning: Very small training set; model is only a pipeline sanity check.

## Recommendations

- Increase candidate diversity if this is intended as a production adsorption search.
- Run or attach QE outputs for missing selected jobs; KS labels are the current bottleneck.
- Collect at least 5 parsed_converged KS labels before interpreting the delta model.
