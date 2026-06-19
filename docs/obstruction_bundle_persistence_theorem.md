# Obstruction-Bundle Persistence Theorem (T038′)

## Statement — T038′

Let \(\gamma\) be a smooth Jordan curve and \(Z\) a compact Morse–Bott family of nondegenerate square configurations in a collision-free neighborhood \(U\).

Assume:

1. \(Z\subset\operatorname{int}(U)\)
2. \(0\notin F_\gamma(\partial U)\)
3. \(\ker DF_\gamma|_z = T_zZ\)
4. The cokernel bundle \(E=\operatorname{coker}(DF_\gamma|_Z)\) satisfies \(\langle w_d(E),[Z]_2\rangle\ne0\)
5. Positive collision margin and side-length lower bound in \(U\)

Then every sufficiently small \(C^0\) perturbation of the four window maps has at least one square configuration in \(U\).

**Status:** `T038′ — CONJECTURAL_TARGET`

## Proof route

Lyapunov–Schmidt reduction + mod-2 Euler / Stiefel–Whitney obstruction: if \(\langle w_d(E),[Z]_2\rangle\ne0\), no nowhere-vanishing continuous section of \(E\) exists; every perturbation forces a zero of \(s_H\).

## Why normal index fails

The countermodel \(F(x,y)=(x,0)\) (`morse_bott_persistence_countermodel.md`) shows normal nondegeneracy is insufficient.

## Continuous perturbations

Route A (smooth approximation) or Route C (polynomial window approximation) must preserve boundary exclusion and collision margins in the limit.

Implementation: `euler_class.py`, `obstruction_section.py`.
