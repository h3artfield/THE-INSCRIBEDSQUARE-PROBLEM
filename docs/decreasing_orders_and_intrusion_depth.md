# Decreasing Orders and Intrusion Depth (Directive 039)

Decreasing gate subsequences \(g_{i_1},\ldots,g_{i_k}\) between boundary and parameter order map to intrusion arc geometry:

- nesting;
- common accumulation;
- branching;
- separated centers;
- hull pinching.

Geometry is derived from **planar audit**, not permutation alone.

Compactness extraction (König/diagonal) yields:

- `INFINITE_NESTED_INTRUSION_RAY`;
- `UNBOUNDED_BRANCHING_TREE`;
- `INFINITE_CENTER_SEQUENCE`;
- `NON_JORDAN_HULL_LIMIT`;
- `PARAMETER_DISCONNECTED_LIMIT`.

**Implementation.** `decreasing_order_geometry.py`, `planar_permuton_rigidity.py` (`certify_t074r_planar`)
