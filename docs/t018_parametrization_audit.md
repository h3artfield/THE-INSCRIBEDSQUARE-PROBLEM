# T018 Parametrization Audit (Directive 007R)

**Result:** **Pass**

---

## Common interval \(I_v=[\tau-\delta,\tau+\delta]\)

Polygon and cubic \(S\) share parameter \(t\). On bridges \(B_v\to A_{v+1}\): \(S=P\) pointwise.

---

## Velocity matching

\[
\frac{dS}{dt}(\tau-\delta)=u_-,\qquad\frac{dS}{dt}(\tau+\delta)=u_+,
\]

matching polygon one-sided derivatives on unchanged straight segments. **Full \(C^1\)**, not \(G^1\).

---

## Basepoint (§9)

Parametric seam placed on interior of unchanged edge via `basepoint_edge` convention; not at smoothed corner.

---

## Prior gap (Directive 007)

Quadratic Bézier **velocity mismatch** — **closed** by cubic construction.
