# Normalized Spectral Problem (Directive 003)

## Geometric data

Let γ be a Jordan curve with enclosed area A > 0 and diameter 2R (radius R = Rad(γ)).

Define the **area–diameter ratio**

\[
B = \frac{A}{R^2}, \qquad \kappa = \frac{\pi R^2}{A} = \frac{\pi}{B}.
\]

By the isodiametric inequality, 0 < B ≤ π and κ ≥ 1, with κ = 1 iff γ is a circle (extremal).

**Dimensional check:** [A] = length², [R²] = length², so B and κ are dimensionless. ✓

## Angle and action normalization

Source spectral invariant: ℓ(γ, θ) for θ ∈ [0, π] (GL26, GL24b).

Define

\[
x = \frac{\theta}{\pi} \in [0,1], \qquad g(x) = \frac{\ell(\pi x)}{A}.
\]

**Dimensional check:** ℓ has units of area, A has units of area, so g is dimensionless. ✓

## Source-verified Level-F consequences

From GL26 §1 (Lipschitz, endpoints, monotonicity, triangle inequality):

1. **Endpoints:** g(0) = ℓ(0)/A = 0; g(1) = ℓ(π)/A = 1.

2. **Monotonicity:** g is nondecreasing (monotone increasing in source; closure = nondecreasing).

3. **Lipschitz bound:** |ℓ(θ₁) − ℓ(θ₂)| ≤ (R²/A)|θ₁ − θ₂|. With θ = πx:
   \[
   |g(y) - g(x)| \leq \frac{R^2}{A} \cdot \pi |y - x| = \kappa |y - x|.
   \]

4. **Triangle inequality:** ℓ(θ₁+θ₂) ≤ ℓ(θ₁)+ℓ(θ₂) gives, for x+y ≤ 1,
   \[
   g(x+y) \leq g(x) + g(y).
   \]

Each formula verified against GL26 §1 and GL24b Prop. 3.5–3.6.

## Midpoint quantities

Square angle: x = 1/2 (θ = π/2).

For 0 < h < 1/2:

\[
D_h(g) = \frac{g(\tfrac12 + h) - g(\tfrac12 - h)}{2h}.
\]

\[
D^+(g, \tfrac12) = \limsup_{h \downarrow 0} D_h(g), \quad
D^-(g, \tfrac12) = \liminf_{h \downarrow 0} D_h(g).
\]

## Research questions

1. Do Level-F axioms force D^+(g, 1/2) > 0?
2. Is there a universal positive lower bound on D_h for fixed h?
3. Is D^-(g, 1/2) > 0 forced?
4. Does the answer depend on B (equivalently κ)?
5. Can D_h → 0 while all Level-F axioms hold?

**Important:** Positive midpoint density is a **proposed sufficient** non-collapse criterion (T004 extraction route). It is **not known** to be necessary for an inscribed square.

## Extremal case κ = 1

When κ = 1, Lipschitz gives g(x) ≤ x and g(x) ≥ x on [0,1] (from g(0)=0, g(1)=1), hence **g(x) = x** identically. Therefore D^+(g, 1/2) = 1. Level-F **forces** midpoint nonflatness at the isodiametric extremum.

## Two-invariant normalization

Separate invariants g₁, g₂ from ℓ(·, ·, α) and ℓ(·, ·, β) (GL24 §4.1). Level-F on each plus **indexed duality**:

\[
g_1(x) + g_2(1 - x) = 1 \quad \text{for all } x \in [0,1].
\]

Do **not** set g₁ = g₂ unless proved.

## LP discretization

Even N, x_i = i/N, G_i ≈ g(x_i). Constraints: G₀=0, G_N=1, monotonicity, Lipschitz, triangle inequality on indices. Minimize

\[
D_{N,k} = \frac{G_{N/2+k} - G_{N/2-k}}{2k/N}.
\]

Grid feasibility is **necessary** but not **sufficient** for continuum feasibility; PL extensions must pass dense subadditivity checks (Directive 003 §6).

## Directive 003 outcome (summary)

| Regime | Level-F midpoint forcing |
|--------|--------------------------|
| κ = 1 | **Forced:** g ≡ x, D⁺ = 1 |
| 1 < κ < κ_c | **Forced (positive):** LP infimum > 0 on certified grids |
| κ > κ_c ≈ 1.026 | **Not forced:** exact PL countermodels with D⁺ = 0 |

κ_c depends on grid refinement; continuum certified at κ = 11/10, 2, … via N=160 PL witnesses (see `functional_countermodels.md`).
