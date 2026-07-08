# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all50_adsorption_remote

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 50 | 539.979 | 31.5988 | 236.127 | 31.5988 | 0.152845 | no | 104.76 | 63.7136 |

## Details

### dftpy_pbe_ads

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 50
- energy_raw_mean_signed_error_ev: -539.979
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.979
- energy_aligned_max_abs_error_ev: 102.98
- adsorption_energy_raw_mae_ev: 236.127
- adsorption_energy_raw_rmse_ev: 239.552
- adsorption_energy_raw_mean_signed_error_ev: 236.127
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 236.127
- adsorption_energy_aligned_mae_ev: 31.5988
- adsorption_energy_aligned_rmse_ev: 40.3647
- adsorption_energy_aligned_max_abs_error_ev: 102.98
- adsorption_spearman_energy: 0.152845
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- candidate_runtime_median_seconds: 2.08225
- truth_runtime_median_seconds: 133.27
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
