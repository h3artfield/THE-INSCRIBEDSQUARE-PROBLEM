# Bounded-Gate Join Estimate (Directive 030)

## Exact decomposition

\[
\mathbb A_X = \sum_i \mathbb A_{X^{(i)}} + \tfrac12\sum_{i<j}\Delta_i\wedge\Delta_j
\]

## Bounds

- \(|\Delta_i| \le C_{\mathrm{collar}}\, r(C)\)
- \(q \le Q(M) = 3M\)
- \(|\mathbb A_{\mathrm{join}}| \le J_M(r) = \tfrac12\binom{Q(M)}{2} C_{\mathrm{collar}}^2 r^2\)

Join bound is **independent of internal winding**.

**Implementation.** `bounded_gate_join.j_m_r`, `audit_join_bound`.

**Status.** PROVED_LOCALLY (analytic bound).
