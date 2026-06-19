# Circle Cokernel Bundle

## Ordered family

\[
\gamma(t)=(\cos t,\sin t),\qquad
z(t)=\left(t,t+\frac\pi2,t+\pi,t+\frac{3\pi}{2}\right),\quad t\in\mathbb R/2\pi\mathbb Z.
\]

## Derivative audit

| Quantity | Value |
|----------|-------|
| \(\rank DF_{\gamma,z(t)}\) | **3** (exact, sampled) |
| \(\ker DF\) | \(\mathrm{span}(1,1,1,1)=T_{z(t)}Z\) |
| \(\dim E\) | 1 |

Explicit cokernel covector \(\ell_t\in\ker DF^T\) computed via SVD (`circle_cokernel.py`).

## Monodromy

Parallel transport of \(\ell_t\) once around \(Z\):

**Monodromy sign = +1** (trivial)

## Verdict

```text
CIRCLE_OBSTRUCTION_LINE_TRIVIAL
```

\[
\langle w_1(E),[S^1]_2\rangle = 0.
\]

A constant nonzero section of \(E\) can remove the abstract family (analogous to the \((x,0)\) countermodel).

**Circle family verdict:** `Circle-B` — trivial obstruction bundle; curve-induced perturbations may satisfy additional constraints (T038-Curve).

Local “normal index = 1” does **not** determine this answer.
