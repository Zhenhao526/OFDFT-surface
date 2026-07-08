# Formal Batch Status: mg0001_o_pilot_all36

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_all36_ks_batch.jsonl | 36 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all36_ks_adsorption.jsonl | 36 | 36/36 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 36/36 (100.0%)
- Status counts: `{"parsed_converged": 36}`
- QE runtime: total 4843.51 s, median 135.511 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all36_adsorption_benchmark.json | dftpy_pbe_ads | 36 | 548.521 | 227.584 | 0.150837 | 64.1885 |
| data/reports/benchmarks/mg0001_o_pilot_all36_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 36 |  | 227.584 | 0.150837 | 64.1885 |
| data/reports/benchmarks/mg0001_o_pilot_all36_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 36 |  | 0.466502 | 0.643243 | 64.1885 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
