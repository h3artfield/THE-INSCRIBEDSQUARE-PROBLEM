# Double Spiral — Variation Classification

**Status:** ANALYTIC (Directive 010)

---

## Measure zero

Each finite spiral segment is \(C^1\) (polar graph), hence measure zero. Countable union + \(\{0\}\) \(\Rightarrow\) planar measure zero.

---

## Infinite length

\[
\int_{\theta_0}^{T}\sqrt{r^2+(dr/d\theta)^2}\,d\theta\gtrsim\int \theta^{-1/2}\,d\theta\to\infty.
\]

---

## Infinite 2-variation

Partition at \(\theta_k=\theta_0+k\pi\). For large \(\theta\),

\[
|\gamma_+(\theta+\pi)-\gamma_+(\theta)|\ge c\,r(\theta).
\]

Hence \(\sum_k|\Delta\gamma|^2\gtrsim\sum_k 1/k=\infty\).

---

## Finite \(p\)-variation

For \(p>2\), increments scale like \(r(\theta)\sim\theta^{-1/2}\); \(\sum \theta^{-p/2}\) converges when \(p>2\). **Index:** not finite for \(p\le 2\); infinite for \(p>2\) case needs separate upper bound — **variation index \(=2\)** (critical).

---

## Local monotonicity at origin

**Unresolved** in full Pak/AI sense — infinite rotation at pinch. Do not claim monotonicity without dedicated proof.

---

## Implementation

`src/squarepeg/residual_curves/double_spiral.py` — `two_var_partition_sum`, `opposite_increment_bound`.
