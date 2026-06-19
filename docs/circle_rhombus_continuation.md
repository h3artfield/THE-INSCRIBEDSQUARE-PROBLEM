# Circle Rhombus Continuation

## Family

\[
\gamma_0(t)=(\cos t,\sin t),\quad
z(t)=\left(t,t+\frac\pi2,t+\pi,t+\frac{3\pi}{2}\right),\quad Z=\{z(t):t\in S^1\}.
\]

## Derivative (verified)

\[
DF_{\gamma_0,z(t)}=
\begin{pmatrix}-2&4&-2&0\\0&-2&4&-2\\-2&0&-2&4\\0&0&0&0\end{pmatrix},
\quad \rank DG=3,\quad \ker=\operatorname{span}(1,1,1,1).
\]

## First-order diagonal obstruction

For \(\gamma_\varepsilon=\gamma_0+\varepsilon h\), \(a(t)=\gamma_0(t)\cdot h(t)\):
\[
\delta D_h(t)=4\bigl[a(t)+a(t+\pi)-a(t+\tfrac\pi2)-a(t+\tfrac{3\pi}{2})\bigr],
\qquad
\delta D_h(t+\tfrac\pi2)=-\delta D_h(t).
\]

*Calibration evidence only; not the nonlinear proof.*

## Rhombus continuation

Tubular neighborhood \(U\cong Z\times\overline{D^3}\), \(\tau\)-invariant, collision-free.

Normal boundary margin \(m_G>0\) certified numerically (~0.33 on transverse samples).

For \(\|\gamma-\gamma_0\|_\infty<\eta\) with \(E_G(\eta)<m_G\):
\[
0\notin G_\gamma(\partial_\nu U),\quad R_\gamma=G_\gamma^{-1}(0)\cap U.
\]

Framework: smooth transversality + uniform limit for continuous curves.

Implementation: `circle_rhombus_family.py`, `rhombus_continuation.py`.
