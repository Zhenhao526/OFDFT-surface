# Remote KEDF Adsorption Energy Errors

- System: `Mg(0001)+O` pilot.
- Adsorption energy formula: `E(slab+O) - E(clean slab) - E(O atom)` using the same KEDF variant for all three terms.
- KSDFT truth: QE/PBE parsed adsorption energy from `mg0001_o_pilot_all50_ks_adsorption.jsonl`.
- Current strict comparison includes variants with completed KEDF references: WT, MGP, MGPA, LMGP.
- Remote load was high; ignore runtime here and focus on energy/error only.

## Summary

| variant | KEDF | n | MAE(eV) | RMSE(eV) | mean signed error(eV) | ads conv | refs conv |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| wt_heg_sp08_m30 | WT | 1 | 269.314 | 269.314 | 269.314 | no | no |
| mgp_atomic_sp08_m30 | MGP | 1 | 61.633 | 61.633 | 61.633 | no | no |
| mgpa_atomic_sp08_m30 | MGPA | 1 | 148.608 | 148.608 | 148.608 | no | no |
| lmgp_atomic_sp08_m30 | LMGP | 2 | 30.373 | 36.914 | 30.373 | yes | yes |

## Per-Structure

| variant | structure_id | site | h(A) | KEDF Eads(eV) | KSDFT Eads(eV) | signed err(eV) | abs err(eV) | conv ads/slab/O |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| wt_heg_sp08_m30 | fb75a97fd775c76d | top | 1.600 | 265.105 | -4.209 | 269.314 | 269.314 | no/no/yes |
| mgp_atomic_sp08_m30 | fb75a97fd775c76d | top | 1.600 | 57.424 | -4.209 | 61.633 | 61.633 | no/no/yes |
| mgpa_atomic_sp08_m30 | fb75a97fd775c76d | top | 1.600 | 144.399 | -4.209 | 148.608 | 148.608 | no/no/yes |
| lmgp_atomic_sp08_m30 | fb75a97fd775c76d | top | 1.600 | 47.143 | -4.209 | 51.352 | 51.352 | yes/yes/yes |
| lmgp_atomic_sp08_m30 | f67b4fe8525ec26c | top | 2.000 | 4.781 | -4.612 | 9.393 | 9.393 | yes/yes/yes |

## Not Yet Strictly Comparable

These variants have adsorbed-structure energies but no completed same-KEDF clean-slab/O references in this run:
- `hc_atomic_sp08_m30`
- `lmgpa_atomic_sp08_m30`
- `revhc_atomic_sp08_m30`
- `tf_heg_sp08_m100`
- `tfvw_heg_sp08_m100`
