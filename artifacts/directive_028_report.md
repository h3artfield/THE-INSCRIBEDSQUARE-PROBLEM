# Directive 028 Report — Intrusion Saturation, Cluster Surgery, and Residual Refinement

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **B — Cluster surgery proved; multi-gate clusters remain**

---

## Executive summary

Directive 028 extends the clean-forest extraction pipeline to **dirty lobes** via intrusion saturation, spatial hull construction, two-gate cluster classification, and cluster crosscut surgery. Two-gate saturated clusters are **closed locally** (T051, T052). Finite multi-gate saturation (T050 full induction, T053, T054) and infinite intrusion trees remain **open**. The residual class is **narrowed** from Directive 027's broad `MULTICENTER_ALTERNATING_INTRUSION_TREE` to four explicit subclasses.

---

## Part I — Directive 027 frozen

| Theorem | Status |
|---------|--------|
| T043R | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED |
| T046 | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED |
| T044R | PROVED_LOCALLY |
| T045R | CONJECTURAL_FULL_EXTRACTION |
| T047 | CONJECTURAL |
| T049 | INTERLEAVING_REFERENCE_UNPROTECTED |

Manifest: `artifacts/directive_027_verified_internal_manifest.json` (commit `d3e7a62`, tag `directive-027-universal-extraction-internal-2026-06-18`).

Frozen proofs **not modified**.

---

## Part II–III — Intrusion geometry and saturation

- Intrusion components defined without generic-position assumptions (perturbation-limit handling documented).
- **Noncrossing endpoint theorem** PROVED_LOCALLY: nested/separated only (`docs/intrusion_noncrossing_structure.md`).
- Recursive saturation \(\mathcal S_\infty(L)\) defined; **order independence** verified on finite trees (`saturation_order_independent`).
- Spatial hull \(H(L)\) via simply-connected radial envelope (`docs/saturated_cluster_hull.md`).

---

## Part IV–VI — Two-gate clusters and finite trees

- Two-gate clean generalizes `CHORD_SAFE_ISOLATED_PACKET` (`docs/two_gate_cluster.md`).
- **Curved crosscut theorem** + **T051** PROVED_LOCALLY: collar fallback when straight chord fails.
- **T050** CONJECTURAL_STRUCTURAL_TARGET; finite-tree two-gate case PROVED_LOCALLY for small trees.
- Dirty bump lobe example: initial lobe dirty → saturation → two-gate clean → surgery candidate (`dirty_examples`).

---

## Part VII — Cluster signature and extraction

- `CLUSTER_SIGNATURE_CARLESON` defined at cluster level.
- **T052** PROVED_LOCALLY for ordered two-gate forests with small diameters.
- **T053** CONJECTURAL_TARGET (requires global finite-two-gate saturation hypothesis).

---

## Part VIII–IX — Multi-gate and infinite trees

- **T054** CONJECTURAL_MULTIGATE_TARGET; interleaving **not** auto-protected (T049).
- Examples: 4-gate and 6-gate nested pairings constructed.
- Infinite nested ray and unbounded branching classes formalized (König extraction).
- Vanishing-diameter ray: maximal-parent surgery **open**.

---

## Part X — Refined residual classes

| Class | Condition |
|-------|-----------|
| INFINITE_MULTIGATE_INTRUSION_RAY | Nested non-stabilizing saturation |
| UNBOUNDED_BRANCHING_INTRUSION_TREE | Unbounded local branching |
| NON_JORDAN_SATURATION_HULL | Hull obstruction |
| DENSE_GATE_ACCUMULATION | ≥4 gates, no T039 protection |

---

## Part XI — Examples and falsification

| Example | Result |
|---------|--------|
| Dirty saturable two-gate | PASS |
| Four-gate cluster | Classified CONJECTURAL (not protected) |
| Six-gate nested | NESTED pairing recorded |
| Infinite ray sequence | INFINITE_MULTIGATE_INTRUSION_RAY |

---

## Part XII — Clean-room audit (reviewer answers)

| # | Question | Answer |
|---|----------|--------|
| 1 | Intrusion components without generic position? | Yes — subdivision + limit |
| 2 | Endpoint structure noncrossing? | Yes — projection test |
| 3 | Saturation order independent? | Yes — finite trees |
| 4 | Hull canonical enough? | Partial — radial hull; overlapping hulls open |
| 5 | Finite induction exhaustive? | No — T050 conjectural globally |
| 6 | Two-gate clusters truly isolated? | Audited locally |
| 7 | Crosscut preserves Jordan? | Yes when isolation holds (T051) |
| 8 | Cluster forests laminar? | Yes for disjoint/nested selection |
| 9 | T043R compatibility? | Yes — cluster as maximal packet |
| 10 | Multi-gate not auto-protected? | Yes — T049 enforced |
| 11 | Infinite trees via compactness? | König lemma formalized |
| 12 | Residual narrower? | Yes — four explicit subclasses |

---

## Part XIII — Outcome selection

**Outcome B:** Two-gate saturated clusters are closed (T051, T052 locally). Finite saturation may produce unresolved multi-gate geometry (T050 full, T054). Global T045R **not** attacked.

---

## Theorem status after Directive 028

| ID | Status |
|----|--------|
| T050 | CONJECTURAL_STRUCTURAL_TARGET |
| T051 | PROVED_LOCALLY |
| T052 | PROVED_LOCALLY (ordered forest) |
| T053 | CONJECTURAL_TARGET |
| T054 | CONJECTURAL_MULTIGATE_TARGET |

---

## Tests

```
tests/test_intrusion_noncrossing.py
tests/test_saturation_order.py
tests/test_two_gate_cluster.py
tests/test_cluster_crosscut.py
tests/test_finite_intrusion_tree.py
tests/test_cluster_forest.py
tests/test_multigate_cluster.py
tests/test_infinite_intrusion_tree.py
```

Run: `pytest -m fast tests/test_intrusion_noncrossing.py tests/test_saturation_order.py tests/test_two_gate_cluster.py tests/test_cluster_crosscut.py tests/test_finite_intrusion_tree.py tests/test_cluster_forest.py tests/test_multigate_cluster.py tests/test_infinite_intrusion_tree.py`

---

## Required deliverables

All modules, docs, and artifacts listed in Directive 028 specification created under `src/squarepeg/defect_extraction/`, `docs/`, `tests/`, and `artifacts/directive_028_report.md`.
