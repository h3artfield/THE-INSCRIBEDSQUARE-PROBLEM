# Critical Smoothing and Primitive Control (T018 Adaptive)

**Status:** PROVED_LOCALLY (Directive 008R, uses frozen T018)

---

## Setup

Polygon \(P_n=\gamma^{D_n}\), total variation \(L_n=\mathrm{Var}_1(P_n)\), coordinate bound \(M_n\ge\|\xi_{P_n}\|_\infty+1\).

Choose \(\varepsilon_n\to 0\) with

\[
\varepsilon_n(L_n+M_n+\varepsilon_n)<2^{-n}.
\]

Frozen **T018** gives \(S_n\) with \(\|S_n-P_n\|_\infty<\varepsilon_n\), \(\|S_n-P_n\|_{1-var}<\varepsilon_n\), same orientation and common parametrization.

---

## Decomposition (§12)

\[
\int_0^t\xi_{S_n}\,dx_{S_n}-\int_0^t\xi_{P_n}\,dx_{P_n}
=\int_0^t(\xi_{S_n}-\xi_{P_n})\,dx_{S_n}+\int_0^t\xi_{P_n}\,d(x_{S_n}-x_{P_n}).
\]

Bounded-variation bound (no Young at \(q=2\); classical BV on polygons):

\[
\sup_{t\in[0,1]}\left|\int_0^t\xi_{S_n}\,dx_{S_n}-\int_0^t\xi_{P_n}\,dx_{P_n}\right|
\le \varepsilon_n(L_n+M_n+\varepsilon_n).
\]

**Valid when \(L_n\to\infty\)** because \(\varepsilon_n\) is chosen inversely.

---

## Combined with polygon primitive convergence

If \(\sup_t|f_n^P(t)-f(t)|\le\eta_n\to 0\) and smoothing error \(<2^{-n}\), then \(\sup_t|f_n^S(t)-f(t)|\to 0\).

---

## Curve convergence

\[
\|S_n-c\|_\infty\le\|S_n-P_n\|_\infty+\|P_n-c\|_\infty\to 0.
\]

\(S_n\) remain regular \(C^1\) embedded Jordan (T018).

---

## Implementation

`src/squarepeg/rough_area/adaptive_smoothing.py`
