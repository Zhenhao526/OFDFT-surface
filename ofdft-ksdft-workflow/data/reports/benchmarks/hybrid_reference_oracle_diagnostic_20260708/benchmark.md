# KSDFT Benchmark: ksdft

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| wt_refs | 50 | 539.979 | 31.5988 | 236.127 | 31.5988 | 0.152845 | no | 316.162 | 21.1114 |
| wt_slab_ks_o_oracle | 50 | 539.979 | 31.5988 | 77.3621 | 31.5988 | 0.152845 | no |  |  |
| ks_slab_wt_o | 50 | 539.979 | 31.5988 | 378.636 | 31.5988 | 0.152845 | no |  |  |
| ks_refs_oracle | 50 | 539.979 | 31.5988 | 539.979 | 31.5988 | 0.152845 | no |  |  |

## Details

### wt_refs

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
- candidate_runtime_median_seconds: 6.3103
- truth_runtime_median_seconds: 133.27
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f

### wt_slab_ks_o_oracle

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 50
- energy_raw_mean_signed_error_ev: -539.979
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.979
- energy_aligned_max_abs_error_ev: 102.98
- adsorption_energy_raw_mae_ev: 77.3621
- adsorption_energy_raw_rmse_ev: 84.9815
- adsorption_energy_raw_mean_signed_error_ev: 74.7833
- adsorption_energy_raw_max_abs_error_ev: 155.848
- adsorption_energy_offset_ev: 74.7833
- adsorption_energy_aligned_mae_ev: 31.5988
- adsorption_energy_aligned_rmse_ev: 40.3647
- adsorption_energy_aligned_max_abs_error_ev: 102.98
- adsorption_spearman_energy: 0.152845
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- truth_runtime_median_seconds: 133.27
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f

### ks_slab_wt_o

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 50
- energy_raw_mean_signed_error_ev: -539.979
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.979
- energy_aligned_max_abs_error_ev: 102.98
- adsorption_energy_raw_mae_ev: 378.636
- adsorption_energy_raw_rmse_ev: 380.781
- adsorption_energy_raw_mean_signed_error_ev: -378.636
- adsorption_energy_raw_max_abs_error_ev: 481.616
- adsorption_energy_offset_ev: -378.636
- adsorption_energy_aligned_mae_ev: 31.5988
- adsorption_energy_aligned_rmse_ev: 40.3647
- adsorption_energy_aligned_max_abs_error_ev: 102.98
- adsorption_spearman_energy: 0.152845
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- truth_runtime_median_seconds: 133.27
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f

### ks_refs_oracle

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 50
- energy_raw_mean_signed_error_ev: -539.979
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -539.979
- energy_aligned_max_abs_error_ev: 102.98
- adsorption_energy_raw_mae_ev: 539.979
- adsorption_energy_raw_rmse_ev: 541.485
- adsorption_energy_raw_mean_signed_error_ev: -539.979
- adsorption_energy_raw_max_abs_error_ev: 642.959
- adsorption_energy_offset_ev: -539.979
- adsorption_energy_aligned_mae_ev: 31.5988
- adsorption_energy_aligned_rmse_ev: 40.3647
- adsorption_energy_aligned_max_abs_error_ev: 102.98
- adsorption_spearman_energy: 0.152845
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- truth_runtime_median_seconds: 133.27
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
