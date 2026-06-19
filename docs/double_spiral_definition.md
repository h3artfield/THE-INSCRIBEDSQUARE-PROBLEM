# Double Spiral Definition

**Status:** DEFINITION (Directive 010)

---

## Parameters

Fix \(\theta_0\ge 2\pi\), \(\varepsilon>0\) small.

\[
r(\theta)=(1+\theta)^{-1/2},\qquad d(\theta)=\varepsilon(1+\theta)^{-2}.
\]

\[
\gamma_+(\theta)=r(\theta)e^{i\theta},\qquad
\gamma_-(\theta)=\bigl(r(\theta)-d(\theta)\bigr)e^{i\theta}.
\]

---

## Closed curve \(\Gamma_{\mathrm{ds}}\)

1. \(\gamma_+\) from outer endpoint toward origin;
2. common limit point \(0\);
3. \(\gamma_-\) outward in reverse;
4. short outer connector joining outer endpoints.

Asymptotics: \(r(\theta)^2\asymp\theta^{-1}\), \(d(\theta)=o(\theta^{-3/2})\).

---

## Implementation

`src/squarepeg/residual_curves/double_spiral.py`
