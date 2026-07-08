# Formal Batch Status: mg0001_o_pilot_all28

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_all28_ks_batch.jsonl | 28 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all28_ks_adsorption.jsonl | 28 | 28/28 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 28/28 (100.0%)
- Status counts: `{"parsed_converged": 28}`
- QE runtime: total 3776.4 s, median 135.66 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all28_adsorption_benchmark.json | dftpy_pbe_ads | 28 | 553.858 | 222.248 | 0.114943 | 64.2327 |
| data/reports/benchmarks/mg0001_o_pilot_all28_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 28 |  | 222.248 | 0.114943 | 64.2327 |
| data/reports/benchmarks/mg0001_o_pilot_all28_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 28 |  | 0.567106 | 0.487137 | 64.2327 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
