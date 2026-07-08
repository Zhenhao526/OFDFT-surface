# MLDFT/M-OFDFT O2 Chemical-Potential Reference

Date: 2026-07-08

This directory treats the real MLDFT O2 calculation as a separate oxygen
chemical-potential reference. It is intentionally not benchmarked against the
current Mg(0001)+O KSDFT labels because those labels use an isolated atomic-O
reference.

Atomic O and `1/2 O2` are different reference conventions and must not be
identified with each other.

## Reference Record

| quantity | value |
| --- | ---: |
| MLDFT O2 total energy | `-4086.055642290963 eV` |
| energy scale | `0.5` |
| 1/2 MLDFT O2 | `-2043.0278211454815 eV` |
| reference kind | `oxygen_chemical_potential` |
| reference id | `half_o2_mldft_str25_qm9` |

Generated files:

- `mofdft_adsorbate_reference.jsonl`
- `wt_mg_mofdft_adsorbate.jsonl`
- `benchmark_skipped.md`

The hybrid candidate uses:

```text
E_ads^(1/2 O2) = E_WT(Mg slab + O) - E_WT(clean Mg slab) - 1/2 E_MLDFT(O2)
```

## Why No Benchmark Is Reported

The existing truth file
`data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl` uses:

```text
E_ads^(O atom) = E_KS(Mg slab + O) - E_KS(clean Mg slab) - E_KS(O atom)
```

Comparing the half-O2 candidate to those labels would mix reference
conventions. It would mostly measure a constant reference offset rather than
the quality of the adsorbed Mg+O energy.

## Required Truth For This Branch

To benchmark this O2 branch, first build compatible KSDFT labels:

```text
E_ads,KS^(1/2 O2) = E_KS(Mg slab + O) - E_KS(clean Mg slab) - 1/2 E_KS(O2)
```

This requires a KSDFT O2 reference calculation with the same pseudopotential,
XC functional, and spin treatment intended for the surface benchmark. Physical
O2 should be treated as triplet.

After that truth file exists, rerun:

```bash
TRUTH=<o2_referenced_ks_truth.jsonl> \
scripts/build_mofdft_hybrid_from_energy.sh \
  -4086.055642290963 \
  0.5 \
  half_o2_mldft_str25_qm9 \
  O2 \
  data/reports/benchmarks/mofdft_o2_chemical_potential_separate_20260708
```

## Atomic-O Branch

For the current Mg(0001)+O label set, the valid branch remains the atomic-O
reference:

```text
E_ads^(O atom) = E(Mg slab + O) - E(clean Mg slab) - E(O atom)
```

That branch needs an explicit atomic-O reference from QE, DFTpy, or a future
M-OFDFT atomic calculation that correctly handles the open-shell O atom and
uses a compatible energy convention.
