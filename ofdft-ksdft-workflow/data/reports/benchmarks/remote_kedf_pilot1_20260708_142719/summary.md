# Remote KEDF Pilot1 Sweep

- System: `Mg(0001)+O` pilot, 3x3x3 slab, first candidate structure (`top`, h=1.6 A, 28 atoms).
- Calculator base: `configs/calculators/dftpy_mg_o_pbe_wt_atomic_m100.yaml` with per-variant KEDF overrides.
- XC: PBE via remote LibXC.
- Grid spacing: 0.8 A.
- Per-variant timeout: 420 s.
- Note: remote node load was high during this run, so wall times are for feasibility screening, not final speed benchmark.

| variant | KEDF | init | status | converged | iter | reached max | E(eV) | dE vs WT(eV) | Fmax(eV/A) | runtime(s) | elapsed(s) |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| wt_heg_sp08_m30 | WT | heg | ok | no | 30 | yes | -52953.791 | 0.000 | 1306.333 | 125.411 | 129 |
| mgp_atomic_sp08_m30 | MGP | atomic | ok | no | 30 | yes | -52345.303 | 608.488 | 1063.666 | 138.574 | 142 |
| mgpa_atomic_sp08_m30 | MGPA | atomic | ok | no | 30 | yes | -52543.015 | 410.775 | 1181.262 | 138.754 | 142 |
| lmgp_atomic_sp08_m30 | LMGP | atomic | ok | yes | 28 | no | -35470.198 | 17483.593 | 331.715 | 123.951 | 128 |
| lmgpa_atomic_sp08_m30 | LMGPA | atomic | ok | no | 30 | yes | -33673.196 | 19280.595 | 289.933 | 125.817 | 131 |
| hc_atomic_sp08_m30 | HC | atomic | ok | no | 30 | yes | -35077.766 | 17876.025 | 325.763 | 131.750 | 135 |
| revhc_atomic_sp08_m30 | revHC | atomic | ok | yes | 30 | no | -34923.471 | 18030.320 | 285.311 | 137.785 | 142 |
| tfvw_heg_sp08_m100 | TFvW | heg | ok | yes | 28 | no | -31397.580 | 21556.211 | 263.694 | 82.444 | 85 |
| tf_heg_sp08_m100 | TF | heg | ok | yes | 94 | no | -35287.792 | 17665.999 | 310.551 | 400.646 | 405 |

## Immediate Readout

- Runnable records: 9/9.
- Density-converged records: 4/9.
- `MGP/MGPA/LMGP/LMGPA/HC/revHC` all returned successfully on the 28-atom pilot structure under the current DFTpy setup.
- `TF` completed but took close to the per-variant timeout window; treat it as a lower-priority control for now.
