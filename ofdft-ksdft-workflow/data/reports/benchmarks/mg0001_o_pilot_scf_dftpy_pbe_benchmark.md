# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot

- Truth records: 6
- Truth records with energy: 6

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_wt_atomic_m100 | 6 | 580.181 | 38.7596 | -0.2 | no | 12.6124 | 64.0804 |

## Details

### dftpy_pbe_wt_atomic_m100

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 6
- Matched candidate converged records: 6
- Energy pairs: 6
- energy_raw_mean_signed_error_ev: -580.181
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -580.181
- energy_aligned_max_abs_error_ev: 62.7781
- max_force_mae_ev_per_ang: 1320.27
- max_force_rmse_ev_per_ang: 1320.86
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 135.622
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7
