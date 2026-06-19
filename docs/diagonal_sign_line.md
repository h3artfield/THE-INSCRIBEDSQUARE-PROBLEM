# Diagonal Sign Line \(L_\chi\)

## Representation

\(\chi:\mathbb Z_4\to\{\pm1\}\), \(\chi(\tau)=-1\).

**Twisted line bundle:**
\[
L_\chi = U\times_\chi \mathbb R \to \overline U = U/\langle\tau\rangle.
\]

Because \(D_\gamma(\tau u)=-D_\gamma(u)\), on \(G_\gamma^{-1}(0)\) the diagonal defect descends to
\[
\overline D_\gamma : \overline R_\gamma \to L_\chi.
\]

## Distinction from Directive 017

| Bundle | Space | \(w_1\) on circle |
|--------|-------|-------------------|
| Cokernel \(E=\operatorname{coker}(DF)\) | Ordered \(Z\cong S^1\) | **0** (trivial) |
| Sign line \(L_\chi\) | Quotient \(\overline Z\) | **1** (Möbius) |

The cyclic-odd mechanism uses \(L_\chi\), not the ordinary cokernel line.

Implementation: `diagonal_sign_line.py`, `twisted_w1.py`.
