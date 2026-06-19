# Directive 002 Report — Exact Solver Hardening and Certification Gate

**Date:** 2026-06-18  
**Version:** 0.2.0  
**Status:** Complete — fast CI suite passes (35/35)

---

## 1. Enumeration completeness

**Proved (finite polygons):** Yes — written proof in `docs/polygon_solver_completeness.md` (T009).

Every inscribed square arises from a forward cyclic edge quadruple and one of \(J=\pm 90^\circ\). Rank-6 systems yield unique isolated certificates; rank-5 systems are represented by `AffineSquareFamily1D` with exact feasible parameter intervals; interior squares on a 1D family are **not** duplicated as isolated samples unless they occur at certified interval endpoints.

---

## 2. Rank-5 sampling removed

**Yes.** The production solver no longer emits sampled `t` values as the mathematical result.

- `AffineSquareFamily1D` stores `base_point`, `direction`, `feasible_intervals`, `excluded_degenerate_t`, `endpoint_isolated_t`, and `proof_residuals`.
- Isolated `exact` certificates are emitted only for rank-6 solutions and rank-5 **interval endpoints** that pass independent validation.

---

## 3. Rank ≤ 4 representation

Systems with nullspace dimension ≥ 2 return `UnsupportedHigherDimensionalFamily` (via `AffineSquareFamilyND` metadata). **No sampling, no silent discard.**

Exact polytope feasibility for dimension ≥ 2 is **not** implemented (explicit stop condition).

---

## 4. Independent certificate validation

`src/squarepeg/exact_squares/validator.py`:

- Reconstructs vertices from edge parameters only (does not trust stored coordinates).
- Checks edge membership, cyclic order, equal sides/diagonals, perpendicularity, distinct vertices, positive side length.
- Uses **independent** equation assembly (`build_equations_independent`) — separate module path from production `equations.py`.
- Validates `AffineSquareFamily1D` nullspace and particular residuals symbolically at sample parameters.

---

## 5. Exact vs interval certification

| Path | Status |
|------|--------|
| Rational polygons → rank 6 isolated | **Certified exact** |
| Rational polygons → rank 5 family | **Certified exact intervals** |
| Float polygons | **Interval wrapper** returns `unresolved` — no approximate roots promoted to exact |
| Rank ≤ 4 | **Unsupported** (typed, loud) |

---

## 6. Differential testing (SymPy)

`src/squarepeg/exact_squares/sympy_checker.py` — independent SymPy RREF rank/consistency check.

- Compared against production rank on test corpus; mismatches auto-save fixtures to `data/differential_fixtures/`.
- Tests: `tests/test_independent_validation.py`

---

## 7. Remaining unsupported cases

- Rank ≤ 4 positive-dimensional families (2D+ nullspace)
- Full interval certification when a candidate square is not supplied (status `unresolved`)
- Irrational-rotation coordinate roundoff may miss some edge-parameter solutions (documented O003)

---

## 8. Runtime and scaling

Benchmark (`python -m squarepeg.benchmarks.run`):

| Polygon | Vertices | Quadruples | Isolated | Families 1D | Runtime |
|---------|----------|------------|----------|-------------|---------|
| Unit 4×4 | 4 | 512 | 1 | 12 | ~0.5s |
| Regression quad | 4 | 512 | ≥1 | varies | ~0.5s |

**Test tiers:**
- `pytest -m fast` — 35 tests, ~112s (no multi-minute oracle)
- `pytest -m slow` — oracle cross-check, random corpus
- `pytest -m exhaustive` — reserved for grid corpus (future)

Profile breakdown (dominant): edge-quadruple enumeration \(O(n^4)\) + 6×6 rational elimination per quadruple.

---

## 9. Bugs found during Directive 002

| ID | Issue | Fix |
|----|-------|-----|
| F002 | Family sampling | Removed; exact intervals |
| D002-1 | Unbounded `t` endpoints produced invalid `u` | Filter `\|t\| ≤ 10^{12}`; pre-check `u ∈ [0,1]` |
| D002-2 | Test picked first family `(0,0,0,0)` empty | Filter nonempty families |

See `docs/solver_failure_history.md` for F001 (e3 matrix).

---

## 10. Ready for spectral experiments?

**Conditional yes** for finite polygon laboratory:

| Gate | Status |
|------|--------|
| Rank-deficient exact or unsupported | ✅ |
| No family sampling | ✅ |
| Independent validator on corpus | ✅ |
| Regression quadrilateral fixture | ✅ |
| SymPy agreement | ✅ |
| Completeness proof written | ✅ |
| Float → exact promotion blocked | ✅ |

**Do not begin** spectral functional LP until slow/exhaustive tiers are green in your CI environment if you require oracle cross-checks.

---

## Files created/updated

```
src/squarepeg/exact_squares/families.py
src/squarepeg/exact_squares/validator.py
src/squarepeg/exact_squares/sympy_checker.py
src/squarepeg/exact_squares/equations.py
src/squarepeg/intervals/arithmetic.py
src/squarepeg/benchmarks/run.py
docs/polygon_solver_completeness.md
docs/solver_failure_history.md
docs/theorem_ledger.md (T009–T011)
tests/test_family_certificates.py
tests/test_independent_validation.py
tests/test_interval_certificates.py
tests/test_property_based.py
tests/test_regressions.py
data/benchmark_polygons.json
artifacts/benchmark_report.json
artifacts/benchmark_report.md
```

---

## Single most important unresolved issue

Rank ≤ 4 families are **explicitly unsupported** — if a polygon square moduli space requires a 2D or higher affine slice, the laboratory reports `UnsupportedHigherDimensionalFamily` rather than certifying. Whether such systems arise in practice for simple polygons remains to be mapped (Milestone 2 extension).
