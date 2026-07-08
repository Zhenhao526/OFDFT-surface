# Formal Batch Status: mg0001_o_pilot_all12

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_candidates.extxyz | 12 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_ks_batch12.jsonl | 12 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_scf_all12_ks_parsed.jsonl | 12 | 12/12 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 12/12 (100.0%)
- Status counts: `{"parsed_converged": 12}`
- QE runtime: total 1596.71 s, median 134.135 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_wt_atomic_m100 | data/processed/screens/mg0001_o_pilot_dftpy_pbe_wt_atomic_m100.jsonl | 12 | 12 | 25.6249 | 2.13328 |
| dftpy_lda_wt_atomic_m100 | data/processed/screens/mg0001_o_pilot_dftpy_lda_wt_atomic_m100.jsonl | 12 | 12 | 23.1428 | 1.89917 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_adsorption_pbe_lda_benchmark.json | dftpy_pbe_ads | 12 | 539.329 | 236.776 | -0.104895 | 62.3109 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_adsorption_pbe_lda_benchmark.json | dftpy_lda_ads | 12 | 417.251 | 230.955 | -0.104895 | 68.9937 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_dftpy_pbe_cv/benchmark.json | dftpy_pbe_raw_cv | 12 | 539.329 |  | -0.104895 | 62.3109 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_dftpy_pbe_cv/benchmark.json | dftpy_pbe_delta_cv | 12 | 40.9573 |  | -0.153846 | 62.3109 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_ads_cv/benchmark.json | dftpy_pbe_ads_raw_cv | 12 |  | 236.776 | -0.104895 | 62.3109 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_ads_cv/benchmark.json | dftpy_pbe_ads_delta_cv | 12 |  | 1.55864 | 0.300699 | 62.3109 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_lda_ads_cv/benchmark.json | dftpy_lda_ads_raw_cv | 12 |  | 230.955 | -0.104895 | 68.9937 |
| data/reports/benchmarks/mg0001_o_pilot_scf_all12_lda_ads_cv/benchmark.json | dftpy_lda_ads_delta_cv | 12 |  | 1.9054 | 0.195804 | 68.9937 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
