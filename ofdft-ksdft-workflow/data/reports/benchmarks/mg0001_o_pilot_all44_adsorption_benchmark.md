# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all44_adsorption

- Truth records: 44
- Truth records with energy: 44

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads | 44 | 543.994 | 31.9407 | 232.111 | 31.9407 | 0.113883 | no | 92.1424 | 63.9185 |

## Details

### dftpy_pbe_ads

- Candidate records: 60
- Candidate converged records: 60
- Matched records: 44
- Matched candidate converged records: 44
- Energy pairs: 44
- energy_raw_mean_signed_error_ev: -543.994
- energy_raw_max_abs_error_ev: 642.959
- energy_offset_ev: -543.994
- energy_aligned_max_abs_error_ev: 98.9649
- adsorption_energy_raw_mae_ev: 232.111
- adsorption_energy_raw_rmse_ev: 235.775
- adsorption_energy_raw_mean_signed_error_ev: 232.111
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 232.111
- adsorption_energy_aligned_mae_ev: 31.9407
- adsorption_energy_aligned_rmse_ev: 41.4004
- adsorption_energy_aligned_max_abs_error_ev: 98.9649
- adsorption_spearman_energy: 0.113883
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1303.66
- max_force_rmse_ev_per_ang: 1303.79
- candidate_runtime_median_seconds: 2.08156
- truth_runtime_median_seconds: 135.004
- Matched structure ids: f67b4fe8525ec26c, a2330293e814d720, 636c3943e12895cb, 7e0cb75306f47f6f, 9ed899052c1ede60, 0173b205f6a5e0d7, 1b6f66e847adf264, fb75a97fd775c76d, 76c2512dfce874bd, 3495ef2ffd6cb58f
