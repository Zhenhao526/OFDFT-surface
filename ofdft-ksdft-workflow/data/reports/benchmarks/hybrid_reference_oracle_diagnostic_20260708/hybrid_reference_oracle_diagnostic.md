# Hybrid Reference Oracle Diagnostic

Date: 2026-07-08

This report tests the most immediately usable hybrid OFDFT path:

```text
E_ads = E_OFDFT(slab + adsorbate) - E_ref(clean Mg slab) - E_ref(adsorbate)
```

The goal is to estimate whether improving the small-molecule/oxygen reference
with a more accurate method such as M-OFDFT can materially improve adsorption
energies when the Mg-containing part is still evaluated with WT OFDFT.

Important: the KS oxygen reference used here is an oracle diagnostic. It is not
a real M-OFDFT result.

## Inputs

- Adsorbed structures: `data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl`
- KSDFT truth: `data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl`
- WT references: `data/processed/screens/mg0001_o_pilot_references_dftpy_pbe_wt_atomic_m100.jsonl`
- KS references: `data/processed/labels/mg0001_o_pilot_references_scf_ks_parsed.jsonl`

The benchmark matches 50 adsorbed Mg(0001)+O structures against KSDFT/PBE.

## Component Energies

| component | WT/PBE OFDFT (eV) | KSDFT/PBE (eV) | WT - KS (eV) |
| --- | ---: | ---: | ---: |
| clean Mg slab | -52499.793081 | -51885.030980 | -614.762101 |
| isolated O atom | -721.203100 | -559.859822 | -161.343278 |

## Candidate Definitions

| candidate | adsorbed energy | Mg slab reference | O reference |
| --- | --- | --- | --- |
| `wt_refs` | WT | WT | WT |
| `wt_slab_ks_o_oracle` | WT | WT | KS oracle |
| `ks_slab_wt_o` | WT | KS oracle | WT |
| `ks_refs_oracle` | WT | KS oracle | KS oracle |

## Benchmark Summary

| candidate | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | offset (eV) | Spearman | top-1 |
| --- | ---: | ---: | ---: | ---: | --- |
| `wt_refs` | 236.127 | 31.599 | 236.127 | 0.153 | no |
| `wt_slab_ks_o_oracle` | 77.362 | 31.599 | 74.783 | 0.153 | no |
| `ks_slab_wt_o` | 378.636 | 31.599 | -378.636 | 0.153 | no |
| `ks_refs_oracle` | 539.979 | 31.599 | -539.979 | 0.153 | no |

Generated benchmark artifacts:

- `benchmark.json`
- `benchmark.md`
- `benchmark.csv`
- `wt_refs.jsonl`
- `wt_slab_ks_o_oracle.jsonl`
- `ks_slab_wt_o.jsonl`
- `ks_refs_oracle.jsonl`

## Interpretation

Replacing only the O reference with a KS oracle reduces raw adsorption-energy
MAE from 236.127 eV to 77.362 eV. This shows that the oxygen reference carries a
large constant bias in the current WT setup.

However, the aligned MAE, Spearman rank correlation, and top-k metrics are
unchanged for all four candidates. This is expected because replacing slab or
adsorbate references applies the same constant shift to every adsorption
structure. It can improve absolute adsorption-energy offsets, but it cannot
repair the relative ordering of adsorption sites, heights, or configurations.

Using KS slab references while keeping WT adsorbed total energies makes the raw
MAE worse. This is also expected: the clean slab reference is a very large
energy term, and replacing it without consistently improving the adsorbed
slab+O energy overcorrects the adsorption formula.

## Consequence For The Hybrid OFDFT Plan

The most realistic first hybrid path is still useful:

```text
E_ads_hybrid = E_WT(Mg slab + O) - E_WT(Mg slab) - E_MOFDFT(O or O2)
```

But based on this oracle diagnostic, it should be treated primarily as a
reference-energy calibration step. It may reduce absolute raw adsorption-energy
bias if M-OFDFT gives a better isolated oxygen reference, but it will not by
itself improve geometry ranking or site selectivity.

To improve ranking, the next technical step must target the adsorbed
slab+oxygen total energy itself. Practical candidates are:

- run LMGP/MGP/HC-style KEDFs on the adsorbed Mg+O structures and references;
- use WT for the Mg-dominated region only if an embedding or subsystem split is
  introduced;
- train a delta correction on adsorption-energy residuals after the oxygen
  reference is calibrated;
- benchmark O atom and half-O2 reference conventions separately before using
  molecular oxygen thermochemistry.

## Recommended Next Step

Use the explicit molecular-reference adapter:

```text
M-OFDFT O/O2 output -> reference JSONL -> ofks-build-hybrid-adsorption -> KSDFT benchmark
```

Then run two comparisons:

1. WT adsorbed + WT slab + M-OFDFT O atom reference.
2. WT adsorbed + WT slab + 1/2 M-OFDFT O2 reference.

This will separate the physically meaningful molecular reference convention
from the larger adsorbed-interface KEDF error.

Example for a half-O2 molecular reference:

```bash
ofks-build-reference-energy \
  --energy-ev <M_OFDFT_O2_TOTAL_ENERGY_EV> \
  --energy-scale 0.5 \
  --reference-id half_o2_mofdft \
  --adsorbate O \
  --formula O2 \
  --backend mofdft \
  --candidate-name mofdft_o2_reference \
  --reference-convention half_o2 \
  --out data/processed/references/mofdft_half_o2_reference.jsonl
```

The resulting JSONL file can be passed as `--adsorbate-reference` to
`ofks-build-hybrid-adsorption`.
