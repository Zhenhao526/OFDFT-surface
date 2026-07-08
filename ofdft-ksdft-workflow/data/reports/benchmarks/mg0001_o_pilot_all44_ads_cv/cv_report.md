# Delta Cross-Validation Report

- Truth name: `ksdft_qe_pbe_scf_pilot_all44_adsorption_cv`
- Usable records: 44
- Folds: 4 / requested 4
- Ridge alpha: 1.0
- Truth energy key: `ks_adsorption_energy_ev`
- Candidate energy key: `adsorption_energy_ev`
- Corrected energy key: `corrected_adsorption_energy_ev`

## Fold Summary

| fold | train | test | train MAE (eV) | train RMSE (eV) | test ids |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 33 | 11 | 0.270474 | 0.352857 | 0173b205f6a5e0d7, 18799da69ead3be3, 26610f4a86dc91d1, 3495ef2ffd6cb58f, 47925b0a9b788d7c, 5d6c0ab5cb071bfa, 6abb28fe07b26672, 79918021a8153bc5, 888219e924ca87f2, ad9ffa908746cb59, f5b49681ac2ee211 |
| 1 | 33 | 11 | 0.316484 | 0.370792 | 0aa0b2a8b9e7bb13, 189ae59fca9f9df9, 2d9196aa6d7e2257, 3d67f03958e4b24f, 48e13434b8f772fe, 61592c9ce5acb3bd, 6c9de9732ccb462b, 7dbf152ecbb0fdcb, 8e7572963539f914, b3cb5f0906f9a78d, f67b4fe8525ec26c |
| 2 | 33 | 11 | 0.239891 | 0.297029 | 0f49ac057057c823, 1b6f66e847adf264, 306ad89390cf1f45, 3e94dc98e10574a6, 54b710a6fadb6bb5, 636c3943e12895cb, 71b0e55452147998, 7e0cb75306f47f6f, 9ed899052c1ede60, d129ec3f37fc8539, fb75a97fd775c76d |
| 3 | 33 | 11 | 0.296535 | 0.357955 | 122e3255b247ee60, 22438c289ddb70f3, 32673556c4a07276, 46256f03336b7973, 5938799807f78886, 6a8fb628258f00a6, 76c2512dfce874bd, 7e2f1fb6c92ddf2f, a2330293e814d720, edeabe8388606624, fbcecd84fda13ba1 |

## Benchmark

# KSDFT Benchmark: ksdft_qe_pbe_scf_pilot_all44_adsorption_cv

- Truth records: 44
- Truth records with energy: 44

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_pbe_ads_raw_cv | 44 |  |  | 232.111 | 31.9407 | 0.113883 | no | 92.1424 | 63.9185 |
| dftpy_pbe_ads_delta_cv | 44 |  |  | 0.41768 | 0.418528 | 0.746723 | no | 92.1424 | 63.9185 |

## Details

### dftpy_pbe_ads_raw_cv

- Candidate records: 44
- Candidate converged records: 44
- Matched records: 44
- Matched candidate converged records: 44
- Energy pairs: 0
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
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 2d9196aa6d7e2257

### dftpy_pbe_ads_delta_cv

- Candidate records: 44
- Candidate converged records: 44
- Matched records: 44
- Matched candidate converged records: 44
- Energy pairs: 0
- adsorption_energy_raw_mae_ev: 0.41768
- adsorption_energy_raw_rmse_ev: 0.634689
- adsorption_energy_raw_mean_signed_error_ev: -0.0212079
- adsorption_energy_raw_max_abs_error_ev: 2.9748
- adsorption_energy_offset_ev: -0.0212079
- adsorption_energy_aligned_mae_ev: 0.418528
- adsorption_energy_aligned_rmse_ev: 0.634335
- adsorption_energy_aligned_max_abs_error_ev: 2.95359
- adsorption_spearman_energy: 0.746723
- adsorption_top1_match: no
- adsorption_top3_recall: 0
- max_force_mae_ev_per_ang: 1303.66
- max_force_rmse_ev_per_ang: 1303.79
- candidate_runtime_median_seconds: 2.08156
- truth_runtime_median_seconds: 135.004
- Matched structure ids: 0173b205f6a5e0d7, 0aa0b2a8b9e7bb13, 0f49ac057057c823, 122e3255b247ee60, 18799da69ead3be3, 189ae59fca9f9df9, 1b6f66e847adf264, 22438c289ddb70f3, 26610f4a86dc91d1, 2d9196aa6d7e2257
