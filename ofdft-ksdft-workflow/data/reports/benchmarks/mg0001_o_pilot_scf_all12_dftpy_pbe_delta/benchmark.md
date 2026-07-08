# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12

- Truth records: 4
- Truth records with energy: 4

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_raw | 4 | 590.735 | 45.1551 | 0.6 | no | 8.58215 | 64.1033 |
| dftpy_pbe_delta | 4 | 57.8225 | 57.8225 | 0.2 | yes | 8.58215 | 64.1033 |

## Details

### dftpy_pbe_raw

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: -590.735
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -590.735
- energy_aligned_max_abs_error_ev: 84.616
- max_force_mae_ev_per_ang: 1330.2
- max_force_rmse_ev_per_ang: 1330.96
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 139.1
- Matched structure ids: 9ed899052c1ede60, a2330293e814d720, f67b4fe8525ec26c, fb75a97fd775c76d

### dftpy_pbe_delta

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 4
- energy_raw_mean_signed_error_ev: 7.03549
- energy_raw_max_abs_error_ev: 95.0872
- energy_offset_ev: 7.03549
- energy_aligned_max_abs_error_ev: 88.0517
- max_force_mae_ev_per_ang: 1330.2
- max_force_rmse_ev_per_ang: 1330.96
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 139.1
- Matched structure ids: 9ed899052c1ede60, a2330293e814d720, f67b4fe8525ec26c, fb75a97fd775c76d
