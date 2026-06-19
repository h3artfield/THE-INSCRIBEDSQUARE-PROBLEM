# Quantitative Ear Defect Allocation (Directive 030)

## One-step

If \(J_M(r) \le \varepsilon/4\) and \(|\mathbb A_C|\ge\varepsilon\):

\[
\max\{|\mathbb A_E|,|\mathbb A_{C'}|\} \ge \tfrac{3\varepsilon}{8}.
\]

## Shrinking scale (T037 link)

Fixed \(\varepsilon = \varepsilon_0/4\), \(r(C_n)\to0\) implies join negligible for \(r < r_0(M,\varepsilon)\).

Explicit \(c(M) = 1/(4Q(M)) > 0\).

**Implementation.** `quantitative_defect_allocation.one_step_allocation`, `audit_peeling_allocation`.

**Status.** PROVED_LOCALLY.
