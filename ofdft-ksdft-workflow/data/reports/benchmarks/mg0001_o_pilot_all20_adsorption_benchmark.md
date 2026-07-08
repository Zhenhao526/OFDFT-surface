# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all20_adsorption

- Truth records: 20
- Truth records with energy: 20

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 20 | 556.48 | 45.9397 | 219.625 | 45.9397 | 0.0180451 | no | 42.2643 | 63.2504 |

## Details

### dftpy_pbe_ads

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 20
- Matched candidate converged records: 20
- Energy pairs: 20
- energy_raw_mean_signed_error_ev: -556.48
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -556.48
- energy_aligned_max_abs_error_ev: 97.5655
- adsorption_energy_raw_mae_ev: 219.625
- adsorption_energy_raw_rmse_ev: 225.982
- adsorption_energy_raw_mean_signed_error_ev: 219.625
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 219.625
- adsorption_energy_aligned_mae_ev: 45.9397
- adsorption_energy_aligned_rmse_ev: 53.2214
- adsorption_energy_aligned_max_abs_error_ev: 97.5655
- adsorption_spearman_energy: 0.0180451
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1308.83
- max_force_rmse_ev_per_ang: 1309.07
- candidate_runtime_median_seconds: 2.09127
- truth_runtime_median_seconds: 133.972
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
