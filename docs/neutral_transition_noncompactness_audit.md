# Neutral Transition Noncompactness Audit (Directive 052)

For each admissible transition \(\mathcal A_v=(X(v),\{X(w)\},A(v,w),E(v))\), audit geometric data:

- hull diameters, scale ratios, gate increments, center positions;
- wedge, retained-skeleton, sign-grouping, crosscut terms.

Escape labels:

| Label | Meaning |
|-------|---------|
| `SCALE_RATIO_ESCAPE` | child ratio \(\to0\) or \(\to1\) |
| `CHILD_COUNT_ESCAPE` | \(\#\mathrm{Ch}(v_n)\to\infty\) |
| `CENTER_DRIFT_ESCAPE` | center-cover divergence |
| `GATE_COMPLEXITY_ESCAPE` | gate/density blow-up |
| `RETAINED_RESERVE_ESCAPE` | skeleton reserve dominance |
| `SIGN_IMBALANCE_ESCAPE` | sign-grouping drift |
| `NORMALIZATION_DENOMINATOR_COLLAPSE` | \(\Phi\to0\) |

**Module:** `transition_escape_audit.py`  
**Fixture:** `data/regressions/neutral_transition_escape_fixture.json`
