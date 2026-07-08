# Formal Batch Status: mg0001_o

## Inputs

| artifact | path | records | status |
| --- | --- | ---: | --- |
| structures | data/processed/structures/mg0001_o_candidates.extxyz | 12 | present |
| selected KS batch | data/processed/splits/mg0001_o_ks_batch.jsonl | 8 | present |
| KS labels | data/processed/labels/mg0001_o_ks_parsed.jsonl | 8 | 0/8 parsed_converged |
| missing KS jobs | data/processed/splits/mg0001_o_missing_qe.jsonl | 8 | needs QE run |

## KSDFT Completion

- Parsed converged: 0/8 (0.0%)
- Status counts: `{"output_missing": 6, "parse_inconsistent": 1, "parsed_unconverged": 1}`

## Candidate Outputs

| candidate | path | records | converged | total runtime (s) | median runtime (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| dftpy_pbe_wt_atomic_m100 | data/processed/screens/mg0001_o_dftpy_pbe_wt_atomic_m100.jsonl | 12 | 12 | 27.2596 | 2.26037 |

## Benchmarks

- No benchmark reports provided.

## Readiness

- KS labels are incomplete; continue QE runs and re-parse outputs.
- Missing QE jobs remain: 8.
