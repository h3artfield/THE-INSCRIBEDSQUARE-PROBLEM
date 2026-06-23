# Non-Jordan Saturation Exhaustion (Directive 060)

T120 exhausts non-Jordan saturation hull failures from positive-scale, collision, parameter, and infinite-center routing. Every route lands in solved machinery or a named global residual:

- `T062` / protected square
- `FINITE_JORDAN_SPLIT`
- `NON_JORDAN_SATURATION_HULL`
- `PARAMETER_DISCONNECTED_LIMIT`
- `INFINITE_CENTER_GEOMETRY`

No new global residual introduced. T045R remains conjectural.

**Modules:** `t119_non_jordan_reduction.py`, `t120_non_jordan_exhaustion.py`, `directive_060_clean_room.py`

**Status:** T119/T120 PROVED_LOCALLY on fixture — Outcome A.
