# Directive 003R Report — Continuum-Certification Repair

**Date:** 2026-06-18  
**Status:** Complete

---

## Final verdict: **Outcome B — Weak-only countermodel**

Level-F axioms with **nondecreasing** monotonicity (Model W) are insufficient to force D⁺(g, ½) > 0 at κ = 11/10: an explicit PL countermodel exists with exact polyhedral subadditivity certification.

For **strict increasing bijection** (Model S, Jordan Floer application): **no valid countermodel found**; the midpoint-nonflatness question under Model S remains **unresolved**.

---

## 1. Finite-PL obstruction

Proved in `docs/finite_pl_obstruction.md`. Strict finite PL ⇒ D⁺(g, ½) > 0.

Directive 003’s N=160 witness had **flat segments** (weak monotonicity), not strict increase.

---

## 2. Witness inspection (κ = 11/10)

| N | Strict? | Flat at ½? | D⁺ | Cell subadditivity |
|---|---------|------------|-----|-------------------|
| 40 | No | Yes | 0 | **PASS** |
| 80 | No | Yes | 0 | PASS |
| 160 | No | Yes | 0 | **FAIL** |

**Answer:** The N=160 function is **not** a strictly increasing bijection with D⁺=0. It is a **nondecreasing** PL function with a flat interval; T014 as originally stated is **retracted**.

---

## 3. Continuum subadditivity

Replaced M=500 grid with polyhedral cell certification (`continuum_cells.py`). N=40 Model W witness: **820 cells, min H = 0**.

---

## 4. Model W vs Model S

| | Model W | Model S |
|---|---------|---------|
| LP constraint | \(G_{i+1}\ge G_i\) | \(G_{i+1}-G_i\ge\delta>0\) |
| κ=11/10, D⁺=0 | **Yes** (N=40 PL) | **No** |
| Jordan Floer | Not applicable | **Target class** |

---

## 5. Transition regime

κ_c ≈ 1.026 relabeled **FINITE_GRID_OBSERVATION** (N=80). At N=320, κ=1.01 grid optimum is already 0. No continuum threshold inferred.

**Analytic positive regime:** only **κ = 1** proved (g ≡ x).

---

## 6. Indexed duality

Independent replication confirms finite-grid LP behavior. “No improvement” retained as **FINITE_GRID_OBSERVATION** only.

---

## 7. Extraction lemma audit

**PROVED_WITH_STRENGTHENED_HYPOTHESIS** — requires uniform slope bound on approximants for all small h; uniform convergence alone insufficient (diagonal gap). See `docs/midpoint_extraction_audit.md`.

---

## 8. Independent replication

`independent_lp.py` matches primary for κ ∈ {1, 11/10, 101/100} at tested N.

---

## 9. Ledger updates

| Entry | New status |
|-------|------------|
| T012 | PROVED_WITH_STRENGTHENED_HYPOTHESIS |
| T013 | DERIVED (unchanged, valid) |
| T014 | **RETRACTED** |
| T014W | PROVED_LOCALLY (Model W only) |

---

## 10. What is blocked until accepted

Level-S / Level-G / Z₄ research may proceed after acceptance of Outcome B and corrected ledger.

---

## Acceptance checklist

- [x] Finite-PL contradiction resolved
- [x] No grid check labeled continuum certification
- [x] Strict / weak separated
- [x] Surviving countermodel has cell-certified subadditivity
- [x] Transition threshold relabeled
- [x] Extraction lemma quantifiers audited
- [x] Independent LP replication
- [x] Ledger corrected
- [x] Single outcome: **B**
