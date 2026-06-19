# Directive 006 Report — Close the Finite-(p)-Variation Bridge

**Date:** 2026-06-18  
**Status:** Complete  
**Verdict:** **Outcome A — T017 proved**

---

## Summary

Every Jordan curve \(c:S^1\to\mathbb R^2\) with finite \(p\)-variation for some \(1\le p<2\) satisfies AI-PEG-v3 Theorem 1.1 and therefore inscribes every \(\theta\)-rectangle, \(\theta\in(0,\pi)\).

**New solved class:** finite \(p\)-variation Jordan curves with \(p<2\) (includes nonrectifiable examples).

---

## Directive 005 reclassification

| Item | Status |
|------|--------|
| D005 verdict | **OUTCOME B — APPROXIMATION OBSTRUCTION** (historical) |
| Precise gap | PL → \(C^1\) with \(q\)-var convergence |
| Closed by | **T018** (this directive) |

---

## Proof components

| Component | Status | Document |
|-----------|--------|----------|
| BG Thm 2.2 polygonal Jordan | Imported | `boedihardjo_geng_dependency_graph.md` |
| BG Lemma 3.1 q-var convergence | Imported | same |
| Interpolation inequality | Proved | `q_variation_interpolation_proof.md` |
| **T018** \(C^1\) smoothing | Proved | `controlled_c1_polygon_smoothing.md` |
| Young primitive convergence | Proved | `young_primitive_convergence_proof.md` |
| AI-PEG-v3 Thm 1.1 | Imported | `asano_ike_dependency_graph.md` |

---

## Sources pinned

| ID | SHA-256 (prefix) |
|----|------------------|
| AI-PEG-v3 | `84395599…` |
| BG-INTERPOLATION-v2 | `fa8be734…` |

---

## Audits

- `docs/t017_independent_audit.md` — **Pass**
- `docs/t017_novelty_audit.md` — **Immediate unstated synthesis**

---

## Tests

Previously skipped tests **unskipped**; validate formulas and constructions only (not theorems).

89+ fast tests passing.

---

## Acceptance checklist

- [x] D005 classified Outcome B
- [x] BG incorporated accurately
- [x] Polygonal q-var convergence (source + interpolation)
- [x] Common parametrization smoothing
- [x] Regular \(C^1\) Jordan approximants
- [x] Smoothing error \(\to 0\) in q-variation
- [x] Young primitive uniform convergence
- [x] Lifted primitives on compacts
- [x] AI conventions audited
- [x] Independent audit complete
- [x] Single outcome: **A**
