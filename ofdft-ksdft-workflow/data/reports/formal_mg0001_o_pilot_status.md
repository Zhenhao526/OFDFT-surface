# Formal Batch Status: mg0001_o_pilot

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_pilot_candidates.extxyz | 12 | present |
| selected KS batch | data/processed/splits/mg0001_o_pilot_ks_batch.jsonl | 6 | present |
| KS labels | data/processed/labels/mg0001_o_pilot_scf_ks_parsed.jsonl | 6 | 6/6 parsed_converged |
| missing KS jobs |  |  | not provided |

## KSDFT Completion

- Parsed converged: 6/6 (100.0%)
- Status counts: `{"parsed_converged": 6}`
- QE runtime: total 808.208 s, median 135.622 s/structure

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_wt_atomic_m100 | data/processed/screens/mg0001_o_pilot_dftpy_pbe_wt_atomic_m100.jsonl | 12 | 12 | 25.6249 | 2.13328 |

## Benchmarks

| report | algorithm | matched | energy MAE (eV) | adsorption MAE (eV) | Spearman | speedup |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| data/reports/benchmarks/mg0001_o_pilot_scf_dftpy_pbe_benchmark.json | dftpy_pbe_wt_atomic_m100 | 6 | 580.181 |  | -0.2 | 64.0804 |
| data/reports/benchmarks/mg0001_o_pilot_scf_dftpy_pbe_delta/benchmark.json | dftpy_pbe_raw | 2 | 635.89 |  | -1 | 68.067 |
| data/reports/benchmarks/mg0001_o_pilot_scf_dftpy_pbe_delta/benchmark.json | dftpy_pbe_delta | 2 | 65.2601 |  | 1 | 68.067 |

## Readiness

- Batch has KS labels and candidate outputs; ready for benchmark/delta training.
