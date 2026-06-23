# Non-Jordan Hull Taxonomy (Directive 060)

Failure types classified at curve level:

- `PINCHED_HULL`
- `SELF_CONTACTING_BOUNDARY`
- `MULTI_BOUNDARY_SATURATION`
- `NONLOCALLY_CONNECTED_LIMIT`
- `SHARED_GATE_COLLISION_HULL`
- `PARAMETER_MERGED_HULL`
- `INFINITE_CENTER_ACCUMULATION`
- `HARMLESS_QUOTIENT`
- `JORDAN_OK`

True non-Jordan failures are separated from harmless quotient artifacts (`HARMLESS_QUOTIENT` vs `JORDAN_OK`).

**Module:** `non_jordan_hull_taxonomy.py`, `t116_saturation_taxonomy.py`

**Status:** T116 PROVED_LOCALLY on fixture (exhaustive taxonomy; no true non-Jordan hulls).
