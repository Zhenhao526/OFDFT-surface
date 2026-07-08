# KSDFT Benchmark: ksdft_qe_pbe_debug_adsorption

- Truth records: 12
- Truth records with energy: 12

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_atomic_m100_ads | 12 | 532.13 | 50.7345 | 250.771 | 50.7345 | 0.153846 | no | 22.9628 | 9.41489 |

## Details

### dftpy_lda_wt_atomic_m100_ads

- Candidate records: 12
- Candidate converged records: 12
- Matched records: 12
- Matched candidate converged records: 12
- Energy pairs: 12
- energy_raw_mean_signed_error_ev: 532.13
- energy_raw_max_abs_error_ev: 598.34
- energy_offset_ev: 532.13
- energy_aligned_max_abs_error_ev: 118.204
- adsorption_energy_raw_mae_ev: 250.771
- adsorption_energy_raw_rmse_ev: 257.679
- adsorption_energy_raw_mean_signed_error_ev: 250.771
- adsorption_energy_raw_max_abs_error_ev: 316.982
- adsorption_energy_offset_ev: 250.771
- adsorption_energy_aligned_mae_ev: 50.7345
- adsorption_energy_aligned_rmse_ev: 59.2626
- adsorption_energy_aligned_max_abs_error_ev: 118.204
- adsorption_spearman_energy: 0.153846
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1260.3
- max_force_rmse_ev_per_ang: 1260.98
- candidate_runtime_median_seconds: 1.9008
- truth_runtime_median_seconds: 17.4152
- Matched structure ids: d6956ca864e76798, d934123ad1c64e6c, a2a22756ea7d51da, 22a44412cf566eb8, cf3dec1024a17bba, 4dd34df24c37a67f, 17453818539e1161, af93973140fe595b, 4d00370b632fa437, 272134a217800bfb
