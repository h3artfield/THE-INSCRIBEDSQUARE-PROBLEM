# Cyclic-Odd Component Definition

See `cyclic_odd_component.py` and Directive 019 Part III.

A **cyclic-odd protected rhombus component** requires:

1. \([R] \in H_1(U,\partial_\nu U;\mathbb Z_2)\) nonzero (mod-2 rhombus degree)
2. \(\tau\)-invariance of \(G^{-1}(0)\cap U\)
3. Nonzero quotient class \([\overline R]\)
4. Sign line \(L_\chi\) with \(\chi(\tau)=-1\)
5. \(\langle w_1(L_\chi),[\overline R]\rangle=1\)
6. Positive collision, side, and rhombus-boundary margins

Does **not** assume the zero set is a manifold for arbitrary continuous \(\gamma\).

Unit circle: certified via `circle_cyclic_odd_component()`.
