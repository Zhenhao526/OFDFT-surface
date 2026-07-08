# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all16_adsorption

- Truth records: 16
- Truth records with energy: 16

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 16 | 550.332 | 51.2764 | 225.774 | 51.2764 | 0.0794118 | no | 33.8757 | 62.679 |

## Details

### dftpy_pbe_ads

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 16
- Matched candidate converged records: 16
- Energy pairs: 16
- energy_raw_mean_signed_error_ev: -550.332
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -550.332
- energy_aligned_max_abs_error_ev: 92.6271
- adsorption_energy_raw_mae_ev: 225.774
- adsorption_energy_raw_rmse_ev: 233.056
- adsorption_energy_raw_mean_signed_error_ev: 225.774
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 225.774
- adsorption_energy_aligned_mae_ev: 51.2764
- adsorption_energy_aligned_rmse_ev: 57.8031
- adsorption_energy_aligned_max_abs_error_ev: 92.6271
- adsorption_spearman_energy: 0.0794118
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1308.68
- max_force_rmse_ev_per_ang: 1308.98
- candidate_runtime_median_seconds: 2.09981
- truth_runtime_median_seconds: 131.882
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
