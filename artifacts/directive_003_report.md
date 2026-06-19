# Directive 003 Report — Spectral Axiom Audit and Midpoint Nonflatness Stress Test

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome type:** (2) Exact countermodel + (1) exact lower bound at κ = 1

---

## Executive summary

Level-F functional axioms extracted from Greene–Lobb and Asano–Ike **do not** force positive midpoint spectral density for all κ ≥ 1. At the isodiametric extremum **κ = 1**, they **do** force D⁺(g, ½) = 1. A sharp transition occurs near **κ_c ≈ 1.026**. Indexed two-invariant duality **does not strengthen** the midpoint bound beyond the one-invariant model.

---

## 1. Source-verified axioms

See `docs/spectral_axiom_ledger.md`. Fifteen property groups audited with exact references. No single-invariant self-duality ℓ(θ)+ℓ(π−θ)=A was encoded.

## 2. One vs two invariants

| Invariant | Level-F properties |
|-----------|-------------------|
| g (single, ℓ₂ normalized) | Endpoints, monotone, κ-Lipschitz, subadditivity |
| g₁, g₂ | Same per component + **g₁(x)+g₂(1−x)=1** (GL24 §4.1 indexed duality) |

## 3. Do Level-F axioms force D⁺ > 0?

**No** for κ ≥ 11/10 (certified continuum PL countermodel).  
**Yes** for κ = 1 (proof g ≡ x).  
**Yes** for 1 < κ < κ_c ≈ 1.026 (LP infimum strictly positive on N=80 grid, exactly verified).

## 4. Dependence on B = A/R²

Yes. κ = π/B. Small B (large κ) weakens Lipschitz, making flat-midpoint countermodels easier. Circle extremum B = π (κ = 1) is the rigid case.

## 5. Extremal case κ = 1

g(x) = x identically; D⁺(g, ½) = 1. Dual certificate: 1-Lipschitz + endpoints (T013).

## 6. Exact certification

All reported LP optima verified with `Fraction` arithmetic via `exact_verify.py`. Float used only inside HiGHS discovery; witnesses re-checked exactly. Continuum subadditivity checked on M=500 rational grid for N=160 PL countermodel.

## 7. Continuum proof / countermodel

| κ | Result |
|---|--------|
| 1 | Proof: g = x |
| 11/10 … 10 | PL countermodel from grid LP, D⁺ = 0 |

Grid-only feasibility explicitly distinguished from continuum (Directive §6).

## 8. Indexed duality

Two-invariant LP: κ=1 → g₂ midpoint optimum 1; κ=11/10 → optimum 0. **No improvement.**

## 9. Weakest additional axiom forcing positivity

Not identified as a single Level-F axiom. Candidate package: **Level S** (derivative property + positive-measure Scholium 2.3) — see `docs/missing_axiom_candidates.md`. Midpoint convexity would force D⁺>0 but is **CONJECTURAL**, not sourced.

## 10. Midpoint extraction lemma

Proved abstractly in `docs/midpoint_extraction_lemma.md` (T012). No derivative-convergence shortcut.

## 11. M001

Benchmark corpus (5 polygons): **zero** rank-≤4 unsupported systems. Recorded in ledger; no classifier implementation.

## 12. Numerical vs proved

| Claim | Status |
|-------|--------|
| κ=1 forcing | DERIVED proof |
| κ≥11/10 countermodel | PROVED_LOCALLY (exact LP + continuum check) |
| κ_c ≈ 1.026 | NUMERICAL_OBSERVATION (bisection, N=80) |
| Real Jordan curve realizing Level-F countermodel | CONJECTURAL / open |
| Midpoint nonflatness for true spectral invariants | CONJECTURE (T005) |

---

## Parameter sweep summary

| κ | LP optimum D_{N,1} | N | Verified |
|---|-------------------|---|----------|
| 1 | 1 | 40 | Yes |
| 101/100 | 81/100 | 40 | Yes |
| 11/10 | 0 | 40 | Yes |
| 5/4, 3/2, 2, 3, 5, 10 | 0 | 40 | Yes |

Full JSON: `experiments/spectral_lp/results/parameter_sweep.json`

---

## Artifacts created

```
src/squarepeg/spectral_axioms/
docs/spectral_axiom_ledger.md
docs/normalized_spectral_problem.md
docs/midpoint_extraction_lemma.md
docs/functional_countermodels.md
docs/missing_axiom_candidates.md
experiments/spectral_lp/
tests/test_spectral_*.py, test_grid_*.py, test_exact_*.py, test_continuum_*.py, test_two_*.py
```

---

## Next theorem target

**Prove Midpoint Nonflatness for actual Jordan Floer spectral invariants** — i.e. show real g from geometry cannot coincide with Level-F countermodels, using Level S/G (derivative property, spectrality, Scholium 2.3, diagonal obstruction). Alternatively, refute by exhibiting a Jordan curve whose spectral invariant satisfies all sourced axioms but has D⁺(g, ½) = 0.

---

## Acceptance checklist

- [x] Every encoded axiom has primary-source reference in ledger
- [x] No false single-invariant self-duality
- [x] Strict monotonicity treated separately (δ family in sweep)
- [x] LP claims exactly verified
- [x] Grid ≠ continuum distinguished
- [x] Continuum countermodel subadditivity checked
- [x] One- and two-invariant models reported separately
- [x] Extraction lemma without derivative convergence
- [x] Proposed axioms marked conjectural
- [x] Precise next theorem target stated
