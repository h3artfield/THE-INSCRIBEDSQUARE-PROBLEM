# Finite p-Variation Source Ledger

Distinct identifiers — do not collapse to generic aliases.

| ID | Reference | Role in T017 |
|----|-----------|--------------|
| **AI-PEG-v3** | Asano–Ike, arXiv:2412.21057v3 (2026-01-05) | Thm 1.1, Remark 5.6 (\(C^1\) sufficient), area normalization |
| **BG-INTERPOLATION-v2** | Boedihardjo–Geng, arXiv:1309.1576v2 | Thm 2.2, Lemma 3.1, Thm 3.1, Thm 3.2 |
| **GL-FLOER-2024** | Greene–Lobb, arXiv:2404.05179 | Background only (not used in T017 chain) |
| **FV-ROUGH-2010** | Friz–Victoir, *Multidimensional Stochastic Processes as Rough Paths* | Young estimates cited by BG |

---

## Pinned files

| Source | PDF | SHA-256 |
|--------|-----|---------|
| AI-PEG-v3 | `data/sources/asano_ike_2412.21057v3.pdf` | `84395599a5ffe4c49e199d128505473c9808e19a6c3b9c3ea052984c1dcf5101` |
| BG-INTERPOLATION-v2 | `data/sources/boedihardjo_geng_1309.1576v2.pdf` | `fa8be7343fa6ae97dff78a62f82a34e1680634c4684469a377d011e1658e73df` |

---

## Statements imported into T017 proof

### From BG-INTERPOLATION-v2

- **Thm 2.2:** simple PL Jordan interpolants, mesh \(\to 0\)
- **Lemma 3.1(2):** \(\|c-c^{\mathcal P}\|_{q\text{-var}}\to 0\) for \(q>p\)
- **Thm 3.1:** Young pairing, constant \(2\zeta(1/p+1/q)\)

### From AI-PEG-v3

- **Thm 1.1:** \(C^0\) + primitive convergence \(\Rightarrow\) all \(\theta\)-rectangles
- **Remark 5.6:** \(C^1\) approximants suffice (measure-zero / general approximation route)
- **Proof of Prop 5.6:** area normalization \(\widetilde c_n=\sqrt{\pi/A_n}\,c_n\)

---

## Locally proved (this directive)

- Interpolation inequality (`docs/q_variation_interpolation_proof.md`)
- **T018** controlled \(C^1\) smoothing (`docs/controlled_c1_polygon_smoothing.md`)
- Young primitive convergence (`docs/young_primitive_convergence_proof.md`)

---

## Directive 005 classification

**OUTCOME B — APPROXIMATION OBSTRUCTION**

Unresolved at end of D005: conversion of BG polygonal interpolants to \(C^1\) Jordan curves with \(q\)-variation convergence.

**Closed in D006** via T018.
