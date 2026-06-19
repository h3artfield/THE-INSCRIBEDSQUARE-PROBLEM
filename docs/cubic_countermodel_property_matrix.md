# Cubic Countermodel Property Matrix

For \(g_*(x)=4x^3-6x^2+3x\), \(\kappa\ge3\).

| Property | Level | g_* status | Notes |
|----------|-------|------------|-------|
| Endpoints g(0)=0, g(1)=1 | F | **Satisfies** | Exact |
| Strict monotonicity / bijection | F | **Satisfies** | g'>0 a.e.; g'=0 only at ½ |
| Lipschitz κ | F | **Satisfies** iff κ≥3 | Lip=3 |
| Subadditivity | F | **Satisfies** | H=12xy(1-x-y)≥0 |
| Indexed duality g(x)+g(1-x)=1 | F | **Satisfies** | g(1-x)=1-g(x); g₁=g₂=g_* |
| Derivative reflection g'(1-x)=g'(x) | F | **Satisfies** | 3(2x-1)² symmetric; F007 |
| Absolute continuity | F | **Satisfies** | C^∞ |
| Differentiability | F | **Satisfies** | C^∞ |
| g'≥0 | F | **Satisfies** | 3(2x-1)² |
| g'>0 a.e. | F | **Satisfies** | Zero only at x=½ |
| Derivative = R(P)² (spectral) | G | **Violates interpretation** | g'(½)=0 ⇒ formal R→0 |
| Pointwise spectrality ∃ rectangle | S | **Cannot evaluate** | Scalar only |
| Finite/locally finite action spectrum | S | **Cannot evaluate** | No Floer complex |
| Floer grading (Maslov) | S | **Cannot evaluate** | — |
| Barcode persistence | S | **Cannot evaluate** | — |
| Continuation-map compatibility | S | **Cannot evaluate** | — |
| Product structure (★) | S | **Cannot evaluate** | — |
| Triangle equality case ℓ(π)=ℓ(π/2)+ℓ(π/2) | S | **Satisfies scalar** | g(1)=2g(½); equality on triangle |
| Diagonal microsupport exclusion | G/S | **Models collapse** | g'(½)=0 = zero radius profile |
| Z₄ square-angle equivariance | G/S | **Not defined** | No source Z₄ action |
| Positive action gap from diagonal | G/S | **Violates if interpreted** | Zero derivative at square angle |

---

## Key collapse signature

\[
g_*\left(\tfrac12\right)=\tfrac12,\qquad g_*'\left(\tfrac12\right)=0.
\]

The collapse signature is the **vanishing derivative**, not the function value at the midpoint.

\[
g_*'(x) = 3(2x-1)^2,\qquad g_*'(1-x)=g_*'(x).
\]

Neither \(g(1-x)=1-g(x)\) nor \(g'(1-x)=g'(x)\) excludes the cubic profile (F007).

If one **formally** identifies \(g_*(x)\) with a normalized spectral invariant and \(g_*'(x)\) with squared rectangle radius at angle \(\pi x\), then at \(x=\tfrac12\) (square angle):

\[
R_{\pi/2}^2 = 0 \quad \text{(formal)}.
\]

This is exactly the **collapse profile** the square program must exclude geometrically. No claim that such rectangles arise from a Jordan curve.

---

## What g_* evades

Level-F scalar axioms (Model S, κ≥3). It does **not** evade:

- Spectral realizability (Level S)
- Geometric radius-as-derivative (Level G, T003)
- Diagonal / microlocal obstructions (AI24)
- Generator-level product rigidity

---

## Half-angle equality

\(g_*(1)=2g_*(½)=1\) saturates subadditivity at \((\tfrac12,\tfrac12)\). See `docs/half_angle_equality_audit.md`.
