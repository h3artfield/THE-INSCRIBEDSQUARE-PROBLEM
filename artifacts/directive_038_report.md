# Directive 038 Report — Nonsummable Order Tails and Planar Permuton Rigidity

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **B — Concentrated and finite-center nonsummable tails closed; genuinely diffuse permutons remain**

---

## Executive summary

Directive 038 classifies positive-inversion laminations not covered by T073I. Intrinsic nonsummability is defined decomposition-independently via \(\mathcal T_*(N,\delta)\). Cross-block interaction measures and T076 trichotomy separate concentrated, finite-center, and diffuse branches. Realizable gate permutations are distinguished from arbitrary permutations; T074R and T077 remain conjectural. T045R unchanged.

---

## Part I — Directive 037 frozen

Manifest: `artifacts/directive_037_verified_internal_manifest.json`.

| ID | Status |
|----|--------|
| T073 | PROVED_LOCALLY |
| T073I | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED |
| T075 | PROVED_LOCALLY (summable class) |
| T074R | CONJECTURAL |
| T072S / T065C | CONJECTURAL / partial |
| T045R | CONJECTURAL_FULL_EXTRACTION |

Frozen modules not modified: T068I, T070, T073, T073I, T075.

---

## Part II–III — Intrinsic nonsummability and interaction measures

- \(\mathcal T_{\mathcal D}(N,\delta)\) and \(\mathcal T_*(N,\delta)\) in `intrinsic_order_tail.py`.
- `NONSUMMABLE_ORDER_TAIL` independent of greedy T075 decomposition.
- \(\Xi_n\), \(\Sigma_n(J;N)\), failure classification in `order_interaction_measure.py`.

---

## Part IV — T076 concentration–compactness

Subsequence classification:

1. **CONCENTRATED_ORDER_INTERACTION** — PROVED_LOCALLY_CLASSIFIER (T064/T064D route).
2. **FINITE_CENTER_ORDER_INTERACTION** — PROVED_LOCALLY_CLASSIFIER (T062 route).
3. **DIFFUSE_ORDER_INTERACTION** — open residual.
4. **INFINITE_INTRUSION_OR_NONJORDAN** — conjectural structural target.

---

## Part V–VI — Realizable permutations and permuton rigidity

- \(\mathcal P_{\mathrm{Jordan}}\) audit: outerplanar gate graph + noncrossing conventions.
- Forbidden patterns 2413/3142: **UNRESOLVED** (reconnaissance only).
- Augmented permuton \(\widetilde\mu_n\) with spatial and scale data.
- T077: `CONJECTURAL_RIGIDITY_TARGET`; summable countably supported limits route to T073I.

---

## Part VII–IX — Intrusion depth, infinite-center, parameter-disconnected

- T074R v2 partial classifier via LDS / nested-arc geometry.
- Infinite-center label reconciled to `INFINITE_WIDTH_INFINITE_CENTER_LAMINATION`.
- T072C partial via T076 branches.

---

## Part X — T065P

Permuton-level diffuse reduction routes summable cases to T073I; nonsummable cases to T076/T077 residuals.

---

## Part XII — Clean-room reviewer answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Nonsummability decomposition-independent? | **Yes** — inf over \(\mathfrak D(L)\) |
| 2 | Interaction measure captures cross-block area? | **Partial** — wedge-pair proxy |
| 3 | Concentration–compactness exhaustive? | **No** — diffuse branch open |
| 4 | Concentrated interaction → valid blocks? | **Yes** — classifier routes T064 |
| 5 | Finite-center reduction uniform? | **Partial** — K-center bound |
| 6 | Realizable permutations topologically characterized? | **Partial** — outerplanar audit |
| 7 | Unbounded width → nested depth or branching? | **Partial** — T074R classifier |
| 8 | Augmented permuton compactness valid? | **Partial** — atom extraction |
| 9 | Countably supported limits → T073I when summable? | **Yes** |
| 10 | Genuinely diffuse residual precise? | **Yes** — definition in T077 |
| 11 | Infinite-center labels reconciled? | **Yes** |
| 12 | T045R still conjectural? | **Yes** |

---

## Outcome B

T076 concentrated and finite-center branches closed at classifier level. Genuinely diffuse Jordan gate permutons remain as explicit residual pending T077.

---

## Theorems

| ID | Status |
|----|--------|
| T076 | CONJECTURAL_STRUCTURAL_TARGET; concentrated + finite-center PROVED_LOCALLY_CLASSIFIER |
| T077 | CONJECTURAL_RIGIDITY_TARGET |
| T074R | CONJECTURAL_STRUCTURAL_TARGET; partial (v2) |
| T072C | CONJECTURAL_TARGET; partial |
| T065P | CONJECTURAL_TARGET; partial |
| T045R | CONJECTURAL_FULL_EXTRACTION |

---

## Residual ledger (updated)

Closed for summable class (D037) and T076 concentrated/finite-center routes.

Open:

- `GENUINELY_DIFFUSE_JORDAN_GATE_PERMUTON`
- `INFINITE_WIDTH_INFINITE_CENTER_LAMINATION` (when T076 diffuse)
- `INFINITE_INTRUSION_TREE`
- `NON_JORDAN_WINDING_LAMINATION`
- `PARAMETER_DISCONNECTED_WINDING_LAMINATION`

---

## Tests

11 passed (D038) + 13 passed (D037 regression) = 24 passed.

**Modules:** `intrinsic_order_tail.py`, `order_interaction_measure.py`, `nonsummable_concentration.py`, `realizable_gate_permutations.py`, `forbidden_pattern_audit.py`, `augmented_gate_permuton.py`, `permuton_rigidity.py`, `intrusion_depth_from_order.py`, `infinite_center_order.py`, `nonsummable_order_reduction.py`
