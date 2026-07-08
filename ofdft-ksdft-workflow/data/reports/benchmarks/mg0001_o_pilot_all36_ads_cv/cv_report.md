# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all36_adsorption_cv`
- Usable records: 36
- Folds: 4 / requested 4
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 27 | 9 | 0.272615 | 0.36517 | 0173b205f6a5e0d7, 22438c289ddb70f3, 3495ef2ffd6cb58f, 47925b0a9b788d7c, 5d6c0ab5cb071bfa, 6c9de9732ccb462b, 7dbf152ecbb0fdcb, 9ed899052c1ede60, d129ec3f37fc8539 |
| 1 | 27 | 9 | 0.358135 | 0.402277 | 0aa0b2a8b9e7bb13, 26610f4a86dc91d1, 3d67f03958e4b24f, 48e13434b8f772fe, 61592c9ce5acb3bd, 71b0e55452147998, 7e0cb75306f47f6f, a2330293e814d720, f67b4fe8525ec26c |
| 2 | 27 | 9 | 0.314802 | 0.377837 | 0f49ac057057c823, 306ad89390cf1f45, 3e94dc98e10574a6, 54b710a6fadb6bb5, 636c3943e12895cb, 76c2512dfce874bd, 7e2f1fb6c92ddf2f, ad9ffa908746cb59, fb75a97fd775c76d |
| 3 | 27 | 9 | 0.282236 | 0.339056 | 1b6f66e847adf264, 32673556c4a07276, 46256f03336b7973, 5938799807f78886, 6abb28fe07b26672, 79918021a8153bc5, 8e7572963539f914, b3cb5f0906f9a78d, fbcecd84fda13ba1 |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all36_adsorption_cv

- Truth records: 36
- Truth records with energy: 36

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 36 |  |  | 227.584 | 33.9922 | 0.150837 | no | 75.4577 | 64.1885 |
| dftpy_pbe_ads_delta_cv | 36 |  |  | 0.466502 | 0.484067 | 0.643243 | no | 75.4577 | 64.1885 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 36
- Candidate converged records: 36
- Matched records: 36
- Matched candidate converged records: 36
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 227.584
- adsorption_energy_raw_rmse_ev: 231.889
- adsorption_energy_raw_mean_signed_error_ev: 227.584
- adsorption_energy_raw_max_abs_error_ev: 317.191
- adsorption_energy_offset_ev: 227.584
- adsorption_energy_aligned_mae_ev: 33.9922
- adsorption_energy_aligned_rmse_ev: 44.4736
- adsorption_energy_aligned_max_abs_error_ev: 94.4375
- adsorption_spearman_energy: 0.150837
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1304.5
- max_force_rmse_ev_per_ang: 1304.65
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.511
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 32673556c4a07276, 3495ef2ffd6cb58f, 3d67f03958e4b24f

### dftpy_pbe_ads_delta_cv

- Candidate records: 36
- Candidate converged records: 36
- Matched records: 36
- Matched candidate converged records: 36
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.466502
- adsorption_energy_raw_rmse_ev: 0.697126
- adsorption_energy_raw_mean_signed_error_ev: -0.104773
- adsorption_energy_raw_max_abs_error_ev: 3.01183
- adsorption_energy_offset_ev: -0.104773
- adsorption_energy_aligned_mae_ev: 0.484067
- adsorption_energy_aligned_rmse_ev: 0.689207
- adsorption_energy_aligned_max_abs_error_ev: 2.90706
- adsorption_spearman_energy: 0.643243
- adsorption_top1_match: no
- adsorption_top3_recall: 0.333333
- max_force_mae_ev_per_ang: 1304.5
- max_force_rmse_ev_per_ang: 1304.65
- candidate_runtime_median_seconds: 2.08091
- truth_runtime_median_seconds: 135.511
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 306ad89390cf1f45, 32673556c4a07276, 3495ef2ffd6cb58f, 3d67f03958e4b24f
