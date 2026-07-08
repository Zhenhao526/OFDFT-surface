# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all12_adsorption

- Truth records: 4
- Truth records with energy: 4

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw | 4 |  |  | 185.37 | 45.1551 | 0.6 | no | 8.58215 | 64.1033 |
| dftpy_pbe_ads_delta | 4 |  |  | 3.80556 | 4.32458 | 0.4 | no | 8.58215 | 64.1033 |

## Details

### dftpy_pbe_ads_raw

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 185.37
- adsorption_energy_raw_rmse_ev: 192.885
- adsorption_energy_raw_mean_signed_error_ev: 185.37
- adsorption_energy_raw_max_abs_error_ev: 269.986
- adsorption_energy_offset_ev: 185.37
- adsorption_energy_aligned_mae_ev: 45.1551
- adsorption_energy_aligned_rmse_ev: 53.3155
- adsorption_energy_aligned_max_abs_error_ev: 84.616
- adsorption_spearman_energy: 0.6
- adsorption_top1_match: no
- adsorption_top3_recall: 0.666667
- max_force_mae_ev_per_ang: 1330.2
- max_force_rmse_ev_per_ang: 1330.96
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 139.1
- Matched structure ids: 9ed899052c1ede60, a2330293e814d720, f67b4fe8525ec26c, fb75a97fd775c76d

### dftpy_pbe_ads_delta

- Candidate records: 4
- Candidate converged records: 4
- Matched records: 4
- Matched candidate converged records: 4
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 3.80556
- adsorption_energy_raw_rmse_ev: 6.22052
- adsorption_energy_raw_mean_signed_error_ev: -3.63305
- adsorption_energy_raw_max_abs_error_ev: 12.2822
- adsorption_energy_offset_ev: -3.63305
- adsorption_energy_aligned_mae_ev: 4.32458
- adsorption_energy_aligned_rmse_ev: 5.04934
- adsorption_energy_aligned_max_abs_error_ev: 8.64916
- adsorption_spearman_energy: 0.4
- adsorption_top1_match: no
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1330.2
- max_force_rmse_ev_per_ang: 1330.96
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 139.1
- Matched structure ids: 9ed899052c1ede60, a2330293e814d720, f67b4fe8525ec26c, fb75a97fd775c76d
