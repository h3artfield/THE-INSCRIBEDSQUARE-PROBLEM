# Curve-Induced Circle Obstruction Sections

## Perturbation subspace

A curve perturbation \(\gamma\mapsto\gamma+h\) induces

\[
s_h(t)=\pi_{E_t}\bigl(D_\gamma F[h](z(t))\bigr),
\]

not an arbitrary section of \(E\).

## Computation (unit circle)

For small radial bump \(h(t)=(0.1\cos t,0.1\sin t)\):

- \(\|s_h\|_\infty \sim 10^{-10}\) (numerically near zero)
- Mean \(\approx 0\)
- Curve-induced sections lie in \(\mathrm{im}(D_\gamma F|_Z)\)

## T038-Curve (conjectural)

> Every sufficiently small **curve-induced** perturbation of the unit circle yields an obstruction section \(s_h:S^1\to E\) with at least one zero.

Possible mechanisms (to be proved, not assumed):

- Zero mean / symmetry constraints on \(\mathrm{im}(D_\gamma F)\)
- Anti-periodicity under cyclic relabeling
- Forced sign change on \(S^1\)

**Status:** `CONJECTURAL` — not proved in Directive 017.

Abstract constant cokernel section **can** remove the family; curve perturbations do not realize arbitrary sections.

Implementation: `curve_induced_section.py`.
