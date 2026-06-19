# Admissible Protected Invariant (Directive 019 update)

\[
\rho_\square^{\mathrm{adm}}(\gamma)
\]

includes **only**:

1. Isolated Brouwer-degree components
2. Proved Euler-obstruction Morse-Bott components (T038′ when fully proved)
3. Proved cyclic-odd components (T039)

**Excludes:** T038′ components without full abstract proof; rank-only families; normal-index-only certificates.

## Cyclic-odd radius

\[
\rho_\square^{\mathrm{cyc}}(\gamma,C)
\]

= largest certified \(C^0\) radius preserving rhombus continuation, \(w_1\) pairing, collision/side margins.

Circle: `rho_square_cyc()` ≈ 0.014 (qualitative).

Implementation: `admissible_radius.py`
