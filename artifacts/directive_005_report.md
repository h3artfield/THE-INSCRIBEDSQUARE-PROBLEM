# Directive 005 Report — Source-Locked Microlocal Reduction

**Date:** 2026-06-18  
**Status:** Complete  
**Verdict:** **Outcome B — Approximation obstruction**

---

## Part I — Directive 004 corrections

| Item | Result |
|------|--------|
| \(g_*(1/2)\) | **1/2** (not 0) |
| Collapse signature | \(g_*'(1/2)=0\) |
| \(g_*'(1-x)=g_*'(x)\) | **True** — F007 logged |
| Synthetic conclusion | Symmetry compatible; neither action nor derivative reflection excludes \(g_*\) |

Regression: `tests/test_cubic_symmetry_repair.py`

---

## Part II — AI-PEG-v3 reconstruction

- PDF pinned: `data/sources/asano_ike_2412.21057v3.pdf`
- SHA-256: `84395599a5ffe4c49e199d128505473c9808e19a6c3b9c3ea052984c1dcf5101`
- Dependency graph: `docs/asano_ike_dependency_graph.md`
- Notation: `docs/asano_ike_notation_dictionary.md`
- Sublemma B.1 → **SOURCE_REPRODUCTION / CALIBRATION**

---

## Part III — T016 residual target

Stated in source notation: `docs/residual_square_angle_vanishing.md`  
Status: **CONJECTURAL_TARGET**

---

## Part IV — T017 bridge program

| Step | Status |
|------|--------|
| p-variation definition | Done (code + docs) |
| Koch nonrectifiable example | Demonstrated (exploratory) |
| Simple polygonal Jordan approximants | **NOT PROVED** |
| q-variation convergence | **NOT PROVED** |
| C¹ smoothing | **NOT PROVED** (source: Remark 5.5 allows C¹) |
| Young primitive convergence | **NOT PROVED** |
| Apply Theorem 1.1 | Blocked |

---

## Outcome B — Missing lemma (exact)

> **T017-A (Approximation Lemma).** For a Jordan parametrization \(c:S^1\to\mathbb{R}^2\) with \(|c|_{p\text{-var}}<\infty\) for some \(1\le p<2\), and for fixed \(q\in(p,2)\), there exists a sequence of **simple** Jordan curves \(c_n\) (polygonal or \(C^1\)) such that:
> 1. \(c_n\to c\) uniformly on \(S^1\);
> 2. \(\|c_n-c\|_{q\text{-var}}\to 0\);
> 3. Enclosed areas converge (after AI-PEG-v3 normalization).

Chord polygons from arbitrary dense samples **do not** automatically yield simplicity — this is the first obstruction.

---

## Part V — Computational support

`src/squarepeg/variation/` — exploratory tools only; not proofs.

---

## Report answers (§IX)

1. Cubic corrections applied; \(g_*(1/2)=1/2\)
2. AI-PEG-v3 chain reconstructed
3. T016 stated (CONJECTURAL)
4. T017 blocked at approximation
5. Koch example: nonrectifiable ⊂ finite p-var class
6. **Outcome B** selected unambiguously
7. Next sublemma: **T017-A** above
8. Calibration (not new microlocal theorem) is immediate AI work

---

## Acceptance checklist

- [x] Cubic errors corrected + F007
- [x] Derivative symmetry tested permanently
- [x] B.1 reclassified
- [x] AI dependency chain exact
- [x] T016 in source notation
- [x] p-variation defined
- [x] Simple approximation not assumed
- [x] Primitive convergence not claimed proved
- [x] No numerical variation as proof
- [x] Single outcome: **B**
