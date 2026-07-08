# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all28_adsorption

- Truth records: 28
- Truth records with energy: 28

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 28 | 553.858 | 37.004 | 222.248 | 37.004 | 0.114943 | no | 58.7924 | 64.2327 |

## Details

### dftpy_pbe_ads

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 28
- Matched candidate converged records: 28
- Energy pairs: 28
- energy_raw_mean_signed_error_ev: -553.858
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -553.858
- energy_aligned_max_abs_error_ev: 94.9431
- adsorption_energy_raw_mae_ev: 222.248
- adsorption_energy_raw_rmse_ev: 227.174
- adsorption_energy_raw_mean_signed_error_ev: 222.248
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 222.248
- adsorption_energy_aligned_mae_ev: 37.004
- adsorption_energy_aligned_rmse_ev: 47.0523
- adsorption_energy_aligned_max_abs_error_ev: 94.9431
- adsorption_spearman_energy: 0.114943
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1306.72
- max_force_rmse_ev_per_ang: 1306.9
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.66
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
