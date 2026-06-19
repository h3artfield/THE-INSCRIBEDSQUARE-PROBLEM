# Ledger Deficit Semicontinuity (Directive 050)

Audit direction for each \(\delta_k\) under equality-core convergence:

| Ledger ID | Direction |
|-----------|-----------|
| WEDGE_PRODUCT | LOWER_SEMICONTINUOUS |
| TRIANGLE_NORM | LOWER_SEMICONTINUOUS |
| CAUCHY_SCHWARZ | CONTINUOUS_UNDER_CORE_CONVERGENCE |
| CHILD_INCREMENT | UPPER_SEMICONTINUOUS |
| HULL_DIAMETER | CONTINUOUS_UNDER_CORE_CONVERGENCE |
| CROSSCUT_AREA | LOWER_SEMICONTINUOUS |
| **RETAINED_SKELETON** | **NOT_CLOSED** |
| CENTER_PACKING | UPPER_SEMICONTINUOUS |
| FINITE_CENTER_GROUP | UPPER_SEMICONTINUOUS |
| **SIGN_GROUPING** | **NOT_CLOSED** |
| CORONA_TRUNCATION | LOWER_SEMICONTINUOUS |
| MULTIGEN_PACKING | LOWER_SEMICONTINUOUS |

`all_closed_for_equality = false`. Repairs: carry auxiliary wedge vectors; replace sign-grouping by closed relaxation.

Uniform \(\delta_k^{(n)}\to0\) on a core would imply simultaneous equality only when every deficit is closed in the needed direction.

**Module:** `deficit_semicontinuity.py`
