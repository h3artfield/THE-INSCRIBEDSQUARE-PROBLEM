# Directive 032 Report — Dense-Gate Winding Layers and Concentration–Compactness

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **B — Concentrated and finite-center branches closed; diffuse laminations remain**

---

## Executive summary

Directive 032 converts dense-gate fixed defect into unbounded normalized winding. **T063** classifies concentrated / diffuse / multicenter regimes. **T062** (finite-center) and **T064** (concentrated descent) are proved locally. **DIFFUSE_NONCROSSING_WINDING_LAMINATION** remains the diffuse residual. T045R unchanged.

---

## Part I — Directive 031 frozen

Manifest: `artifacts/directive_031_verified_internal_manifest.json`.

---

## Part II–III — Normalization and winding

- \(\mathbb A_{\widetilde Z_n}=\varepsilon_0/r_n^2\to\infty\).
- Closed walk \(\widehat Z_n\); chord correction bounded.
- \(|w_n|_{L^\infty}\gtrsim C_{\mathrm{iso}}|\mathbb A_{\widetilde Z_n}|\).
- Layer-cake identity and winding-layer tree.

---

## Part IV–V — T063 concentration-compactness

PROVED_LOCALLY as exhaustive classifier (discrete planar version).

---

## Part VI — T064 concentrated descent

Consecutive parameter blocks with fixed defect fraction; original scale \(o(r_n)\).

PROVED_LOCALLY when parameter-consecutive.

`DISCONNECTED_CONCENTRATION` for spatial-only balls.

---

## Part VII–VIII — T062 complete; diffuse layers

- **T062 PROVED_LOCALLY** for \(\le K\) centers.
- Diffuse: unbounded layer depth; scale-ratio branches.
- Scale jumps return to T064.

---

## Part IX — Lamination residual

`DIFFUSE_NONCROSSING_WINDING_LAMINATION` defined precisely.

Surgery on ordered two-gate leaves partial; protected geometry open.

---

## Part X–XI — T061R and T065

T061R replaces implementation-label T061.

T065: finite-tree reduction partial — concentrated + finite-center closed; diffuse lamination open.

---

## Part XII — Falsification

| Example | Branch |
|---------|--------|
| Small square winding | CONCENTRATED |
| Spiral chain | DIFFUSE |
| Separated centers | MULTICENTER / T062 |
| Non-consecutive spatial ball | DISCONNECTED |

---

## Part XIII — Clean-room

12 questions answered; T045R conjectural; infinite trees separate.

---

## Outcome B

T062 + T064 proved locally. Diffuse winding laminations remain.

---

## Theorems

| ID | Status |
|----|--------|
| T063 | PROVED_LOCALLY (classifier) |
| T064 | PROVED_LOCALLY (consecutive) |
| T062 | PROVED_LOCALLY (finite-center) |
| T061R | CONJECTURAL_REFINEMENT / classifier |
| T065 | CONJECTURAL_TARGET |

---

## Tests

13 passed (D032) + 14 passed (D031 regression).
