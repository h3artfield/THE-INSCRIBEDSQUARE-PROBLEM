# Polygonal 2-Variation Dynamic Program

**Status:** PROVED_LOCALLY (Directive 009)

---

## Vertex optimality (p > 1)

For a polygonal path with fixed vertices \(v_0,\ldots,v_N\) in order, the supremum

\[
|\alpha|_{p-var}^p=\sup_{\Pi}\sum_i|\Delta\alpha_i|^p
\]

is achieved on a partition whose break points are among \(\{v_j\}\) and the endpoints.

**Proof:** refining any subinterval \([t_i,t_{i+1}]\) by an interior vertex \(v_k\) replaces one increment by two; for \(p>1\), \(|a+b|^p\le|a|^p+|b|^p\) with equality only when collinear degeneracy — maximum sum uses vertex breaks.

---

## Squared 2-variation DP

Define

\[
F(j)=\max_{0\le i<j}\bigl(F(i)+|v_j-v_i|^2\bigr),\quad F(0)=0.
\]

Then

\[
|\alpha|_{2-var;[0,t_N]}^2=F(N).
\]

---

## Implementation

`src/squarepeg/area_variation/exact_2variation.py`

Rational exact mode via `Fraction` vertices.
