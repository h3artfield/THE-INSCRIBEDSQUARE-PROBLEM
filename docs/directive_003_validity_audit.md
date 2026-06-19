# Directive 003 Validity Audit (003R)

**Date:** 2026-06-18  
**Auditor:** Independent repair pass (Directive 003R)

---

## Summary of errors in Directive 003

| Claim | Verdict |
|-------|---------|
| T014 continuum countermodel at κ≥11/10 | **RETRACTED** (as stated) |
| N=160 PL with D⁺=0 and M=500 grid subadditivity | **INVALID** as continuum certificate |
| κ_c ≈ 1.026 | **FINITE_GRID_OBSERVATION** (N=80 only) |
| Level-F insufficient for all κ>1 | **CONDITIONAL_ON_CONTINUUM_COUNTERMODEL** |
| Indexed duality no improvement | **FINITE_GRID_OBSERVATION** only |
| T013 g≡x at κ=1 | **VALID** (analytic proof) |
| T012 extraction lemma | **PROVED_WITH_STRENGTHENED_HYPOTHESIS** |

---

## Witness inspection (κ=11/10)

### N=40 (Model W — valid weak countermodel)

| Property | Value |
|----------|-------|
| Strictly increasing | **No** (13 flat segments) |
| Flat interval at ½ | [19/40, 21/40], slope 0 |
| \(D_h\) at \(h=1/40\) | 0 |
| \(D^+(g,½)\) (continuum) | **0** (flat segment) |
| Lipschitz constant | 11/10 (saturated) |
| Endpoints | 0, 1 |
| Continuum subadditivity (cell cert) | **PASS** (820 cells, min H = 0) |
| Strict bijection with D⁺=0 | **No** |

### N=160 (Directive 003 “certificate”)

| Property | Value |
|----------|-------|
| Flat at ½ | Yes |
| Continuum subadditivity (cell cert) | **FAIL** (5 violations, min H = −49/9600) |
| Valid countermodel | **No** |

**Cause of apparent D⁺=0:** flat PL segment under weak monotonicity; LP objective at fixed grid scale; not strict bijection.

---

## Model W vs Model S

| Model | Monotonicity | κ=11/10, D⁺=0 |
|-------|--------------|----------------|
| W (nondecreasing) | \(G_{i+1}\ge G_i\) | **Yes** — N=40 PL with cell cert |
| S (strict bijection) | \(G_{i+1}-G_i\ge\delta>0\) | **No** finite-grid or finite-PL witness; obstruction lemma |

Jordan Floer source (GL26) states **monotone increasing bijection** → **Model S** for the application.

---

## Independent LP replication

Second implementation in `independent_lp.py` matches primary optimum and witnesses for κ∈{1, 11/10, 101/100} at tested N.

---

## Final verdict selection

See `artifacts/directive_003R_report.md` — **Outcome B**.
