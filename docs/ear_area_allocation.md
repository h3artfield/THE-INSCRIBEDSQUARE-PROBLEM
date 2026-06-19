# Ear Area Allocation (Directive 029)

## Exact decomposition

\[
\mathcal A_C = \mathcal A_E + \mathcal A_{C'} + \mathcal A_{\mathrm{join}}
\]

Join term explicit via Chen wedge at gate increments:

\[
\mathcal A_{\mathrm{join}} = \tfrac12 \Delta(g_a,g_b) \wedge \Delta_{\mathrm{junction}}
\]

**Implementation.** `ear_area_allocation.decompose_ear_area`.

## Quantitative alternative

For \(|\mathcal A_C|\ge\varepsilon\) and \(2m\) gates, either:
1. ear carries \(\ge c(m)\varepsilon\);
2. join carries \(\ge c(m)\varepsilon\);
3. remainder retains fixed fraction.

\(c(m)=1/m\) recorded; **global bound not closed** (Outcome B).

Join defect classified via `audit_defect_allocation` — not discarded as bookkeeping.
