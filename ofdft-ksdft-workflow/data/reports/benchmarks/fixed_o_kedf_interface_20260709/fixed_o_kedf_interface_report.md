# Fixed Atomic-O KEDF Interface Benchmark

This benchmark uses one calibrated atomic-O reference for every KEDF variant:

```text
E_ads = E_KEDF(Mg slab + O) - E_KEDF(clean Mg slab) - E_fixed(O)
```

The goal is to focus the comparison on the adsorbed Mg+O and clean-slab KEDF energies after the atomic-O reference has been fixed.

Caveat: current KEDF coverage is sparse. One-structure variants have meaningless aligned MAE and ranking metrics; read their raw adsorption error only. Multi-structure ranking conclusions require more completed slab+adsorbed pairs.

## Adsorbate Reference

- reference_id: `o_atom_mldft_str25_qm9_pseudo_calibrated_to_qe_o_atom`
- total_energy_ev: `-559.8598218127081`

## Benchmark

# KSDFT Benchmark: ksdft_fixed_o

- Truth records: 50
- Truth records with energy: 50

## Summary

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| lmgp_atomic_sp08_m30 | 2 | 16957.9 | 20.9797 | 126.034 | 20.9797 | 1 | yes |  |  |
| wt_heg_sp08_m30 | 1 | 504.691 | 0 | 107.976 | 0 |  | yes |  |  |
| mgp_atomic_sp08_m30 | 1 | 103.797 | 0 | 61.2045 | 0 |  | yes |  |  |
| mgpa_atomic_sp08_m30 | 1 | 93.9159 | 0 | 24.2873 | 0 |  | yes |  |  |

## Details

### lmgp_atomic_sp08_m30

- Candidate records: 2
- Candidate converged records: 2
- Matched records: 2
- Matched candidate converged records: 2
- Energy pairs: 2
- energy_raw_mean_signed_error_ev: 16957.9
- energy_raw_max_abs_error_ev: 16978.9
- energy_offset_ev: 16957.9
- energy_aligned_max_abs_error_ev: 20.9797
- adsorption_energy_raw_mae_ev: 126.034
- adsorption_energy_raw_rmse_ev: 127.769
- adsorption_energy_raw_mean_signed_error_ev: 126.034
- adsorption_energy_raw_max_abs_error_ev: 147.014
- adsorption_energy_offset_ev: 126.034
- adsorption_energy_aligned_mae_ev: 20.9797
- adsorption_energy_aligned_rmse_ev: 20.9797
- adsorption_energy_aligned_max_abs_error_ev: 20.9797
- adsorption_spearman_energy: 1
- adsorption_top1_match: yes
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 281.635
- max_force_rmse_ev_per_ang: 284.899
- truth_runtime_median_seconds: 135.972
- Matched structure ids: f67b4fe8525ec26c, fb75a97fd775c76d

### wt_heg_sp08_m30

- Candidate records: 1
- Candidate converged records: 0
- Matched records: 1
- Matched candidate converged records: 0
- Energy pairs: 1
- energy_raw_mean_signed_error_ev: -504.691
- energy_raw_max_abs_error_ev: 504.691
- energy_offset_ev: -504.691
- energy_aligned_max_abs_error_ev: 0
- adsorption_energy_raw_mae_ev: 107.976
- adsorption_energy_raw_rmse_ev: 107.976
- adsorption_energy_raw_mean_signed_error_ev: 107.976
- adsorption_energy_raw_max_abs_error_ev: 107.976
- adsorption_energy_offset_ev: 107.976
- adsorption_energy_aligned_mae_ev: 0
- adsorption_energy_aligned_rmse_ev: 0
- adsorption_energy_aligned_max_abs_error_ev: 0
- adsorption_top1_match: yes
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1299.26
- max_force_rmse_ev_per_ang: 1299.26
- truth_runtime_median_seconds: 128.263
- Matched structure ids: fb75a97fd775c76d

### mgp_atomic_sp08_m30

- Candidate records: 1
- Candidate converged records: 0
- Matched records: 1
- Matched candidate converged records: 0
- Energy pairs: 1
- energy_raw_mean_signed_error_ev: 103.797
- energy_raw_max_abs_error_ev: 103.797
- energy_offset_ev: 103.797
- energy_aligned_max_abs_error_ev: 0
- adsorption_energy_raw_mae_ev: 61.2045
- adsorption_energy_raw_rmse_ev: 61.2045
- adsorption_energy_raw_mean_signed_error_ev: -61.2045
- adsorption_energy_raw_max_abs_error_ev: 61.2045
- adsorption_energy_offset_ev: -61.2045
- adsorption_energy_aligned_mae_ev: 0
- adsorption_energy_aligned_rmse_ev: 0
- adsorption_energy_aligned_max_abs_error_ev: 0
- adsorption_top1_match: yes
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1056.59
- max_force_rmse_ev_per_ang: 1056.59
- truth_runtime_median_seconds: 128.263
- Matched structure ids: fb75a97fd775c76d

### mgpa_atomic_sp08_m30

- Candidate records: 1
- Candidate converged records: 0
- Matched records: 1
- Matched candidate converged records: 0
- Energy pairs: 1
- energy_raw_mean_signed_error_ev: -93.9159
- energy_raw_max_abs_error_ev: 93.9159
- energy_offset_ev: -93.9159
- energy_aligned_max_abs_error_ev: 0
- adsorption_energy_raw_mae_ev: 24.2873
- adsorption_energy_raw_rmse_ev: 24.2873
- adsorption_energy_raw_mean_signed_error_ev: 24.2873
- adsorption_energy_raw_max_abs_error_ev: 24.2873
- adsorption_energy_offset_ev: 24.2873
- adsorption_energy_aligned_mae_ev: 0
- adsorption_energy_aligned_rmse_ev: 0
- adsorption_energy_aligned_max_abs_error_ev: 0
- adsorption_top1_match: yes
- adsorption_top3_recall: 1
- max_force_mae_ev_per_ang: 1174.19
- max_force_rmse_ev_per_ang: 1174.19
- truth_runtime_median_seconds: 128.263
- Matched structure ids: fb75a97fd775c76d


## Skipped Variants

- `lmgpa_atomic_sp08_m30`: missing clean slab structure_id=d78831db0d40c74b
- `hc_atomic_sp08_m30`: missing slab-reference input
- `revhc_atomic_sp08_m30`: missing slab-reference input
- `tf_heg_sp08_m100`: missing slab-reference input
- `tfvw_heg_sp08_m100`: missing slab-reference input
