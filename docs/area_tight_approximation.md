# Area-Tight Approximation

**Status:** DEFINITION (Directive 010)

---

## Polygonal relative area

For simple polygonal Jordan \(P_n=(x_n,\xi_n)\) and cyclically ordered \((s,t)\):

\[
\mathcal A_{P_n}(s,t)=\frac12\int_s^t\Bigl[(x_n-x_n(s))\,d\xi_n-(\xi_n-\xi_n(s))\,dx_n\Bigr].
\]

Same sign convention as T021 / 008R audit.

---

## Area-tight sequence

\((P_n)\) is **area-tight** when:

1. \(P_n\to c\) uniformly;
2. each \(P_n\) is a simple closed polygonal Jordan map, fixed orientation;
3. \[
   \lim_{\delta\downarrow 0}\limsup_{n\to\infty}\sup_{d_{S^1}(s,t)\le\delta}|\mathcal A_{P_n}(s,t)|=0.
   \]

Finite initial terms irrelevant.

---

## Relation to rough paths

Area-tightness is **weaker** than Yang canonical enhancement convergence along all partitions. It requires only **one** good approximating sequence for Asano–Ike.

---

## T022

See `docs/area_tight_rectangular_peg_criterion.md`.
