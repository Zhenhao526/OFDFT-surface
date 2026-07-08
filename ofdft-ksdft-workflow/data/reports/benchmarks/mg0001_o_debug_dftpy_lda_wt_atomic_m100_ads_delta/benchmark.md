# KSDFT Benchmark: ksdft_qe_pbe_debug_adsorption

- Truth records: 5
- Truth records with energy: 5

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_ads_raw | 5 | 246.128 | 58.5113 | 0.7 | no | 9.4915 | 9.76351 |
| dftpy_lda_ads_delta | 5 | 1.60504 | 1.55454 | -0.5 | no | 9.4915 | 9.76351 |

## Details

### dftpy_lda_ads_raw

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 246.128
- adsorption_energy_raw_rmse_ev: 254.944
- adsorption_energy_raw_mean_signed_error_ev: 246.128
- adsorption_energy_raw_max_abs_error_ev: 315.774
- adsorption_energy_offset_ev: 246.128
- adsorption_energy_aligned_mae_ev: 58.5113
- adsorption_energy_aligned_rmse_ev: 66.4657
- adsorption_energy_aligned_max_abs_error_ev: 113.561
- adsorption_spearman_energy: 0.7
- adsorption_top1_match: no
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1268.75
- max_force_rmse_ev_per_ang: 1269.77
- candidate_runtime_median_seconds: 1.89991
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c

### dftpy_lda_ads_delta

- Candidate records: 5
- Candidate converged records: 5
- Matched records: 5
- Matched candidate converged records: 5
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 1.60504
- adsorption_energy_raw_rmse_ev: 1.70665
- adsorption_energy_raw_mean_signed_error_ev: -0.252492
- adsorption_energy_raw_max_abs_error_ev: 2.26706
- adsorption_energy_offset_ev: -0.252492
- adsorption_energy_aligned_mae_ev: 1.55454
- adsorption_energy_aligned_rmse_ev: 1.68787
- adsorption_energy_aligned_max_abs_error_ev: 2.14985
- adsorption_spearman_energy: -0.5
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1268.75
- max_force_rmse_ev_per_ang: 1269.77
- candidate_runtime_median_seconds: 1.89991
- truth_runtime_median_seconds: 18.6074
- Matched structure ids: af93973140fe595b, c0e80c3f8db2ae82, cf3dec1024a17bba, d6956ca864e76798, d934123ad1c64e6c
