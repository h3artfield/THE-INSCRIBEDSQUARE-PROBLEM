# Augmented Gate Permutons (Directive 038)

## Geometric permuton

For each truncation, define augmented measure \(\widetilde\mu_n\) on

\[
S^1_{\partial}\times S^1_{\mathrm{par}}\times\overline{B(0,1)}\times[0,\infty),
\]

recording boundary order, parameter order, normalized spatial gate position, and geometric scale weight.

Weak limits are extracted as atom lists with support class:

- `COUNTABLY_MONOTONE_SUPPORTED`
- `NONSUMMABLE_GRAPH_SUPPORTED`
- `GENUINELY_DIFFUSE`

Summable graph-supported limits route to T073I.

**Implementation.** `augmented_gate_permuton.py`
