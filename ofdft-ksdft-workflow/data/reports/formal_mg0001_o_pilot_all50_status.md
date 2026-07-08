# Formal Batch Status: mg0001_o_pilot_all50

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz | 48 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_all50_ks_batch.jsonl | 50 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl | 50 | 50/50 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 50/50 (100.0%)
- Status counts: `{"parsed_converged": 50}`
- QE runtime: total 6674.64 s, median 133.27 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_ads | data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl | 60 | 60 | 125.599 | 2.08156 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_all50_adsorption_benchmark.json | dftpy_pbe_ads | 50 | 539.979 | 236.127 | 0.152845 | 63.7136 |
| data/reports/benchmarks/mg0001_o_pilot_all50_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 50 |  | 236.127 | 0.152845 | 63.7136 |
| data/reports/benchmarks/mg0001_o_pilot_all50_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 50 |  | 0.325418 | 0.827323 | 63.7136 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
