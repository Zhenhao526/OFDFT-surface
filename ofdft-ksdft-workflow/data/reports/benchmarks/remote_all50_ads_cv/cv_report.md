# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all50_adsorption_remote_cv`
- Usable records: 50
- Folds: 5 / requested 5
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 40 | 10 | 0.275655 | 0.336715 | 0173b205f6a5e0d7, 18799da69ead3be3, 26610f4a86dc91d1, 3d67f03958e4b24f, 54b710a6fadb6bb5, 6a8fb628258f00a6, 79918021a8153bc5, 888219e924ca87f2, ad9ffa908746cb59, f36b1bcd35c8bdf9 |
| 1 | 40 | 10 | 0.281079 | 0.331257 | 0199c00b22820d26, 189ae59fca9f9df9, 2d9196aa6d7e2257, 3e94dc98e10574a6, 5938799807f78886, 6abb28fe07b26672, 7dbf152ecbb0fdcb, 8e7572963539f914, b3cb5f0906f9a78d, f5b49681ac2ee211 |
| 2 | 40 | 10 | 0.258113 | 0.300844 | 0aa0b2a8b9e7bb13, 1b6f66e847adf264, 306ad89390cf1f45, 46256f03336b7973, 5d6c0ab5cb071bfa, 6c9de9732ccb462b, 7e0cb75306f47f6f, 9a7283fc61f1d6da, d129ec3f37fc8539, f67b4fe8525ec26c |
| 3 | 40 | 10 | 0.258257 | 0.307858 | 0f49ac057057c823, 2086432d65d5b674, 32673556c4a07276, 47925b0a9b788d7c, 61592c9ce5acb3bd, 71b0e55452147998, 7e2f1fb6c92ddf2f, 9ed899052c1ede60, e83ef44dd4753136, fb75a97fd775c76d |
| 4 | 40 | 10 | 0.283985 | 0.334966 | 122e3255b247ee60, 22438c289ddb70f3, 3495ef2ffd6cb58f, 48e13434b8f772fe, 636c3943e12895cb, 76c2512dfce874bd, 8656ded82956740a, a2330293e814d720, edeabe8388606624, fbcecd84fda13ba1 |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all50_adsorption_remote_cv

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 50 |  |  | 236.127 | 31.5988 | 0.152845 | no | 104.76 | 63.7136 |
| dftpy_pbe_ads_delta_cv | 50 |  |  | 0.325418 | 0.325418 | 0.827323 | no | 104.76 | 63.7136 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 50
- Candidate converged records: 50
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 0
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
- Matched structure ids: 0173b205f6a5e0d7, 0199c00b22820d26, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 2086432d65d5b674, 22438c289ddb70f3

### dftpy_pbe_ads_delta_cv

- Candidate records: 50
- Candidate converged records: 50
- Matched records: 50
- Matched candidate converged records: 50
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.325418
- adsorption_energy_raw_rmse_ev: 0.424436
- adsorption_energy_raw_mean_signed_error_ev: -0.0187516
- adsorption_energy_raw_max_abs_error_ev: 1.58132
- adsorption_energy_offset_ev: -0.0187516
- adsorption_energy_aligned_mae_ev: 0.325418
- adsorption_energy_aligned_rmse_ev: 0.424021
- adsorption_energy_aligned_max_abs_error_ev: 1.56257
- adsorption_spearman_energy: 0.827323
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1302.5
- max_force_rmse_ev_per_ang: 1302.62
- candidate_runtime_median_seconds: 2.08225
- truth_runtime_median_seconds: 133.27
- Matched structure ids: 0173b205f6a5e0d7, 0199c00b22820d26, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 2086432d65d5b674, 22438c289ddb70f3
