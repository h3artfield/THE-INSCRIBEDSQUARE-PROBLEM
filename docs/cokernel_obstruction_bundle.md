# Cokernel Obstruction Bundle

## Morse–Bott data

Let \(F:U\subset\mathbb R^n\to\mathbb R^n\) be \(C^1\) and let \(Z=F^{-1}(0)\cap U\) be a compact \(d\)-dimensional submanifold with

\[
\ker DF_z = T_z Z \quad \forall z\in Z.
\]

## Definition

\[
E_z = \mathbb R^n / \operatorname{im}DF_z.
\]

When \(\rank DF_z = n-d\) is constant on \(Z\), the fibers \(E_z\) assemble into a rank-\(d\) vector bundle \(E\to Z\).

**Regularity:** \(F\in C^1\), constant rank on \(Z\), and local triviality from the implicit function theorem on the normal bundle.

## Normal vs cokernel equations

- \(\dim\ker DF_z = d\)
- \(\rank DF_z = n-d\)
- \(\dim\operatorname{coker}DF_z = d\)

Normal invertibility controls \(n-d\) equations. The remaining \(d\) equations form an obstruction in \(E\).

## Perturbation section

For \(G=F+H\) small, Lyapunov–Schmidt reduction yields a section \(s_H:Z\to E\). Zeros of \(G\) near \(Z\) correspond to zeros of \(s_H\).

See `cokernel_bundle.py`, `obstruction_section.py`.
