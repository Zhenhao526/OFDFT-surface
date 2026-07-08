# Formal Batch Status: mg0001_o_pilot_all20

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_jitter_next8_ks_batch.jsonl | 8 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all20_ks_adsorption.jsonl | 20 | 20/20 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 20/20 (100.0%)
- Status counts: `{"parsed_converged": 20}`
- QE runtime: total 2673.23 s, median 133.972 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all20_adsorption_benchmark.json | dftpy_pbe_ads | 20 | 556.48 | 219.625 | 0.0180451 | 63.2504 |
| data/reports/benchmarks/mg0001_o_pilot_all20_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 20 |  | 219.625 | 0.0180451 | 63.2504 |
| data/reports/benchmarks/mg0001_o_pilot_all20_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 20 |  | 0.959243 | 0.299248 | 63.2504 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
