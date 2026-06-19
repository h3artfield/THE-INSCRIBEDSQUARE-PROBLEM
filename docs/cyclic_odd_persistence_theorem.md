# Cyclic-Odd Persistence Theorem

## Proof chain

1. **Rhombus continuation:** \(R_\gamma=G_\gamma^{-1}(0)\cap U\) persists for small \(\|\gamma-\gamma_0\|_\infty\) when \(E_G(\eta)<m_G\).

2. **Quotient cycle:** \(\overline R_\gamma=R_\gamma/\langle\tau\rangle\) is a 1-cycle pairing nontrivially with \(w_1(L_\chi)\).

3. **Sign obstruction:** \(\langle w_1(L_\chi),[\overline Z]_2\rangle=1\).

4. **Diagonal zero:** If \(\overline D_\gamma\) were nowhere zero on \(\overline R_\gamma\), it would trivialize \(L_\chi|_{\overline R_\gamma\), contradicting (3).

5. **Square:** \(\exists u\in R_\gamma\) with \(D_\gamma(u)=0\); with \(G_\gamma(u)=0\) and collision margin, \(u\) is a nondegenerate square.

## Continuous curves

Smooth stage first; then \(\gamma_n\to\gamma\) uniformly with \(\gamma_n\) smooth Jordan. Compact \(U\) ⇒ subsequence \(u_n\to u\), \(F_\gamma(u)=0\) by continuity.

Implementation: `cyclic_odd_persistence.py`, `continuous_curve_limit.py`.
