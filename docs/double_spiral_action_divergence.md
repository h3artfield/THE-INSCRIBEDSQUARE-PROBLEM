# Double Spiral — Action Divergence

**Status:** ANALYTIC (Directive 010)

---

## One-arm symmetrized action

\[
\frac12\int r(\theta)^2\,d\theta=\frac12\int\frac{d\theta}{1+\theta}\sim\frac12\log T\to\infty.
\]

---

## Liouville convention

Under AI-PEG-v3 \(\lambda=\xi\,dx\), translate via endpoint correction (`docs/critical_area_to_liouville_primitive.md`).

Primitive oscillation grows logarithmically along arm prefix.

---

## Finite enclosed area between arms

\[
\frac12\int\bigl(r_+^2-r_-^2\bigr)d\theta
\approx\varepsilon\int r(\theta)\,d(\theta)\,d\theta
\]

converges (dominated by \(r\sim\theta^{-1/2}\) against \(d\sim\theta^{-2}\)).

**Key:** large cancelling primitive oscillation, finite domain area.

---

## Implementation

`one_arm_action`, `annulus_area_between_arms` in `double_spiral.py`.
