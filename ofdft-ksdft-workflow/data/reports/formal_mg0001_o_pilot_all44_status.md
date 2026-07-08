# Formal Batch Status: mg0001_o_pilot_all44

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_all44_ks_batch.jsonl | 44 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all44_ks_adsorption.jsonl | 44 | 44/44 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 44/44 (100.0%)
- Status counts: `{"parsed_converged": 44}`
- QE runtime: total 5889.61 s, median 135.004 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all44_adsorption_benchmark.json | dftpy_pbe_ads | 44 | 543.994 | 232.111 | 0.113883 | 63.9185 |
| data/reports/benchmarks/mg0001_o_pilot_all44_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 44 |  | 232.111 | 0.113883 | 63.9185 |
| data/reports/benchmarks/mg0001_o_pilot_all44_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 44 |  | 0.41768 | 0.746723 | 63.9185 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
