# Transition Regime Status

## What κ_c was

Directive 003 reported

\[
\kappa_c \in \left(\frac{4201}{4096}, \frac{52513}{51200}\right) \approx (1.0256, 1.0256)
\]

from bisection at **N=80** on the **finite grid LP** (Model W, k=1).

**Label:** `FINITE_GRID_OBSERVATION` — not a continuum threshold.

## Grid refinement study (Model W, k=1)

| N | κ=101/100 optimum | κ=21/20 optimum | κ=11/10 optimum |
|---|-------------------|-----------------|-----------------|
| 40 | 81/100 > 0 | 1/20 > 0 | 0 |
| 80 | 61/100 > 0 | 0 | 0 |
| 160 | 21/100 > 0 | 0 | 0 |
| 320 | **0** | 0 | 0 |

**Conclusions:**

1. The threshold for **positive finite-grid optimum** at κ=101/100 **decreases** with N (81/100 → 61/100 → 21/100 → 0).
2. No numerical stabilization toward a continuum κ_c — apparent bisection at N=80 was **misleading**.
3. At N=320, even κ=1.01 yields grid optimum 0 under Model W.

## What is actually justified

| Statement | Status |
|-----------|--------|
| κ=1 forces g≡x (continuum) | **PROVED** (T013) |
| 1<κ<κ₀ implies D⁺≥c(κ)>0 on continuum | **UNRESOLVED** |
| κ=11/10 allows Model W countermodel | **PROVED** (N=40 PL + cell cert) |
| κ=11/10 allows Model S countermodel | **NOT FOUND** |
| Finite-grid κ_c | **FINITE_GRID_OBSERVATION** only |

## Model S (δ>0)

Any strict gap δ>0 forces positive grid objective at κ=11/10 (e.g. opt=1/25 at δ=1/1000, N=40). Consistent with obstruction lemma; **no transition** in strict class.

## Analytic lower bound attempt

From endpoints + κ-Lipschitz alone: at κ=1, g=x. For κ>1, no continuum lower bound on D⁺ was derived from subadditivity + Lipschitz in this audit. Methods **cannot extend** the κ=1 proof to κ>1 without additional axioms.

**Positive regime:** only κ=1 proved. Interval (1, ∞) for Model S: **unresolved**.
