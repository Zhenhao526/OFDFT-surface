# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_wt_atomic_m100 | 12 | 539.329 | 48.1636 | -0.104895 | no | 25.6249 | 62.3109 |

## Details

### dftpy_pbe_wt_atomic_m100

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: -539.329
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.329
- energy_aligned_max_abs_error_ev: 103.629
- max_force_mae_ev_per_ang: 1307.11
- max_force_rmse_ev_per_ang: 1307.48
- candidate_runtime_median_seconds: 2.13328
- truth_runtime_median_seconds: 134.135
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
