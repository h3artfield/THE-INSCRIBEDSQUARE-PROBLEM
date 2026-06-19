# Directive 011 Report — Double-Spiral Obstruction and Certified Limit Square

**Date:** 2026-06-18  
**Status:** Complete

---

## Verdicts (independent)

| Target | Outcome |
|--------|---------|
| **T024-A** | `T024-A_ONLY_PROVED` (cyclic PL obstruction) |
| **T024-B** | Proved under \(C^1\) convergence; **OPEN** for \(C^0\)-uniform only |
| **T025** | `T025_PROVED_BY_COMPACTNESS` |

---

## Part I — Freeze

Manifest: `artifacts/t022_pre_residual_freeze_manifest.json`  
Frozen: T019, T021, T022 (unchanged proof files)

---

## Part II — Canonical model

**Frozen:** \(\theta_0=2\pi\), \(\varepsilon=1/20\), linear outer connector  
**Hash:** `c535f4e3cc643ed945854ba53d818444245e00c014648625b8603c344d648ae7`  
**Doc:** `docs/double_spiral_canonical_definition.md`

Jordan re-audit: `docs/double_spiral_jordan_proof.md` (unchanged, references canonical)

---

## Part III — T024

### Shrinking tails

\(t(\theta)=r(\theta)/r(\theta_0)\); for \(N_k=M_k^2\), \(|I_k|\to 0\), disk radius \(\to 0\).

### Area growth

\(\frac12\int_M^{M^2}r^2\,d\theta=\frac12\log\frac{1+M^2}{1+M}\ge c\log M-C\).

### T024-A

**Proved:** no area-tight cyclic PL sequence (`docs/double_spiral_no_area_tightness.md`).

### T024-B

**Proved** if \(\|Q_n-\Gamma\|_{C^1}\to 0\) (primitive equicontinuity contradiction).  
**Open** for uniform convergence without derivative control.

---

## Part IV–V — T025

### Branch tracking

Macroscopic branch stable for \(N=3..7\): side/diam \(\approx 0.507\), min radius \(\ge 0.22\).

### Proof

**Compactness route** — uniform exact certificates on truncations + parameter compactness + continuity of square equations.

Interval certificate on smooth pieces: **not obtained** (spurious near-origin roots).

---

## Central conclusion

> The double spiral lies beyond the area-tight / Asano–Ike primitive method but **still contains** a positive-size inscribed square.

See `docs/residual_method_failure_vs_square_existence.md`.

---

## Classification table

| Statement | Status |
|-----------|--------|
| Jordan | proved |
| Infinite length | proved |
| Infinite 2-variation | proved |
| T024-A | **proved** |
| T024-B (\(C^1\)) | **proved** |
| T024-B (\(C^0\)) | open |
| T025 | **proved** (compactness) |
| Square-peg counterexample | **no** |
| Universal area-tightness | **false** (this curve) |

---

## Code added

`protected_annuli.py`, `winding_stability.py`, `primitive_obstruction.py`, `square_branch_tracking.py`, `interval_square_solver.py`, `canonical.py`, `limit_square.py`

---

## Tests

New fast tests for annuli, winding, obstruction, branch tracking, compactness certificate.

**Do not** describe theorems as externally accepted.
