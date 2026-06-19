# Canonical Double-Spiral Definition (Directive 011 — FROZEN)

**Status:** FROZEN  
**Hash:** see `CanonicalDoubleSpiral.definition_hash()`

---

## Frozen parameters

| Parameter | Value |
|-----------|-------|
| \(\theta_0\) | \(2\pi\) |
| \(\varepsilon\) | \(1/20\) |
| \(r(\theta)\) | \((1+\theta)^{-1/2}\) |
| \(d(\theta)\) | \(\varepsilon(1+\theta)^{-2}\) |
| Orientation | CCW |
| Connector | Linear chord from \(\gamma_-(\theta_0)\) to \(\gamma_+(\theta_0)\) |
| Parameter seam | \(u=0\) at \(\gamma_+(\theta_0)\) |

---

## Arms

\[
\gamma_+(\theta)=r(\theta)(\cos\theta,\sin\theta),\qquad
\gamma_-(\theta)=\bigl(r(\theta)-d(\theta)\bigr)(\cos\theta,\sin\theta).
\]

---

## Closed curve \(\Gamma_{\mathrm{ds}}\) (traversal order)

1. **Outer arm** \(\gamma_+\): from \(\theta=\theta_0\) inward to origin;
2. **Origin** (common limit point);
3. **Inner arm** \(\gamma_-\): from origin outward (reverse angular order) to \(\gamma_-(\theta_0)\);
4. **Outer connector**: chord from \(\gamma_-(\theta_0)\) to \(\gamma_+(\theta_0)\).

---

## Circle parametrization (outer arm)

\[
t(\theta)=\frac{r(\theta)}{r(\theta_0)}=\sqrt{\frac{1+\theta_0}{1+\theta}},\qquad t(\theta_0)=1,\quad t(\theta)\to 0^+\text{ as }\theta\to\infty.
\]

Tail intervals \(I_k=[t(N_k),t(M_k)]\) with \(N_k=M_k^2\) satisfy \(|I_k|\to 0\).

---

## Implementation

`src/squarepeg/residual_curves/canonical.py` — **single source of truth**.

All Directive 011 numerics and proofs use this model only.
