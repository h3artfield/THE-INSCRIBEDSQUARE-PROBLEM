# Directive 039 Report — Planar Permuton Rigidity and the Diffuse Order Residual

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **B — Bounded-depth rigidity proved; unbounded depth/branching is the remaining permuton route**

---

## Executive summary

Directive 039 targets the genuinely diffuse Jordan gate-permuton residual from Directive 038. Geometric realizability \(\mathcal P_J\) is defined independently of implementation. **T077-A** is proved locally: bounded depth, branching, and center count forbid genuinely diffuse permuton limits via planar inversion extremal bounds. Full **T077**, **T074R**, and **T065PR** remain conjectural for unbounded sequences. **T045R unchanged.**

---

## Part I — Directive 038 frozen

Manifest: `artifacts/directive_038_verified_internal_manifest.json`.

| ID | Status |
|----|--------|
| T073I | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED |
| T075 | PROVED_LOCALLY |
| T076 | PROVED_LOCALLY (concentrated + finite-center) |
| T074R | CONJECTURAL |
| T077 | CONJECTURAL |
| T045R | CONJECTURAL_FULL_EXTRACTION |

---

## Part II–III — Geometric realizability and finite classification

- Finite Jordan gate system with cyclic permutation extraction.
- \(\mathcal P_J\) invariance under cyclic shift, reversal, deletion, block restriction (classifier).
- Forbidden patterns 2413/3142: **UNRESOLVED** (reconnaissance).
- Planar substitution decomposition tree for realizable orders.

---

## Part IV — Decreasing sequences and T074R

Decreasing subsequence geometry from planar audit (not permutation alone). Compactness extraction with local-finiteness assumptions. T074R partial classifier via `certify_t074r_planar`.

---

## Part V–VIII — Augmented permuton and bounded-depth rigidity

- \(\widetilde\mu_N\) with depth \(d_i\); tightness after hull normalization.
- Five-part genuinely diffuse definition excluding solved branches.
- **T077-A PROVED_LOCALLY:** inversion density \(\le f(D,B,K)\) under bounded geometry.
- Planar inversion graph + crossing-number alternative.

---

## Part IX–XI — T077, residuals, T065PR

T077 routes bounded-depth sequences away from diffuse permutons. Unbounded depth → `INFINITE_INTRUSION_TREE`; unbounded branching → `UNBOUNDED_BRANCHING_INTRUSION_TREE`. T065PR partial: bounded-depth diffuse eliminated.

---

## Part XII — Residual ledger

`GENUINELY_DIFFUSE_JORDAN_GATE_PERMUTON` restricted to **unbounded depth/branching** sequences only.

Remaining universal residuals:

- `INFINITE_INTRUSION_TREE`
- `UNBOUNDED_BRANCHING_INTRUSION_TREE`
- `NON_JORDAN_SATURATION_HULL`
- `PARAMETER_DISCONNECTED_LIMIT`
- `INFINITE_CENTER_THICK_LAMINATION`
- `POSITIVE_SCALE_NONANNULAR_CLUSTER`

---

## Part XIV — Clean-room reviewer answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Realizability independent of implementation? | **Yes** |
| 2 | Cyclic seams handled correctly? | **Yes** |
| 3 | P_J hereditary? | **Partial** — classifier only |
| 4 | Unbounded width → planar geometry? | **Partial** — T074R classifier |
| 5 | Augmented permuton retains needed data? | **Yes** — depth added |
| 6 | Diffuse definition disjoint from solved branches? | **Yes** |
| 7 | Bounded depth constrains order complexity? | **Yes** — T077-A |
| 8 | Extremal planar estimate valid? | **Partial** — local bound |
| 9 | Crossings compatible with shared endpoints? | **Yes** — noncrossing audit |
| 10 | Center and parameter-disconnected separated? | **Yes** |
| 11 | Every diffuse branch routed? | **Partial** — unbounded open |
| 12 | T045R still conjectural? | **Yes** |

---

## Outcome B

T077-A proved locally. Bounded-depth, bounded-branching, finite-center Jordan systems cannot produce genuinely diffuse gate permuton limits. Unbounded depth/branching remains the permuton route to explicit residuals.

---

## Theorems

| ID | Status |
|----|--------|
| T077-A | PROVED_LOCALLY |
| T077 | CONJECTURAL_RIGIDITY_TARGET; partial |
| T074R | CONJECTURAL_TARGET; partial |
| T065PR | CONJECTURAL_TARGET; partial |
| T045R | CONJECTURAL_FULL_EXTRACTION |

---

## Tests

16 passed (D039) + 24 regression (D038–D037) = **40 passed**.

**Modules:** `jordan_gate_realizability.py`, `realizable_permutation_class.py`, `substitution_decomposition.py`, `decreasing_order_geometry.py`, `augmented_permuton_compactness.py`, `bounded_depth_order.py`, `planar_inversion_graph.py`, `permuton_extremal_bound.py`, `planar_permuton_rigidity.py`, `diffuse_permuton_reduction.py`
