# Formal Batch Status: mg0001_o_pilot_all16

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_jitter_next8_ks_batch.jsonl | 8 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all16_ks_adsorption.jsonl | 16 | 16/16 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 16/16 (100.0%)
- Status counts: `{"parsed_converged": 16}`
- QE runtime: total 2123.3 s, median 131.882 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all16_adsorption_benchmark.json | dftpy_pbe_ads | 16 | 550.332 | 225.774 | 0.0794118 | 62.679 |
| data/reports/benchmarks/mg0001_o_pilot_all16_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 16 |  | 225.774 | 0.0794118 | 62.679 |
| data/reports/benchmarks/mg0001_o_pilot_all16_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 16 |  | 0.9571 | 0.270588 | 62.679 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
