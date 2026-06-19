# Rough Area to Liouville Primitive

**Status:** FORMULA REFERENCE (Directive 008)

---

## AI-PEG-v3 convention

\(c=(x,\xi)\), \(\lambda=\xi\,dx\), \(f(t)-f(s)=\int_s^t \xi\,dx\).

---

## Planar geometric 2-rough path

Second level \(\mathbb A(s,t)\in[\mathbb R^2,\mathbb R^2]\) antisymmetric part encodes area:

\[
\mathbb A_{\mathrm{sym}}(s,t) \approx \frac12\int_s^t [x\,d\xi - \xi\,dx] \quad\text{(orientation dependent)}.
\]

**Do not identify** rough area directly with \(\int\xi\,dx\) without symmetric/endpoint corrections.

---

## Recovery formula (PL / smooth)

For smooth or PL \((x,\xi)\):

\[
\int_s^t \xi\,dx = \frac12\Bigl(\int_s^t x\,d\xi + \int_s^t \xi\,dx\Bigr)_{\text{symmetric Young}}
\]

At \(q=2\), use **enhanced** second level from \(\mathcal G_2\), not ordinary Young.

For **classical** \(C^1\) (T017 route): ordinary / Young with \(q<2\) suffices.

---

## T020 requirement

Prove uniform convergence of recovered \(f_n\) from **convergent** second levels \(A(P_n^D)\), not from numeric area alone.

Implementation reference: `src/squarepeg/rough_area/primitive_recovery.py` (exploratory).
