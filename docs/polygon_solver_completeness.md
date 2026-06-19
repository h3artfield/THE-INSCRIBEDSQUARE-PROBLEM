# Polygon Square Solver — Enumeration Completeness

**Scope:** Simple polygons (piecewise-linear Jordan curves) only.  
**Status:** Argument written; labeled `PROVED_LOCALLY` pending full alignment audit with implementation.

---

## Theorem (Finite completeness)

Every nondegenerate square inscribed in a simple polygon \(P\) is represented by at least one cyclic edge quadruple \((e_1,e_2,e_3,e_4)\) examined by the solver, for at least one choice of orientation \(J \in \{+90^\circ,-90^\circ\}\), and is retained after deduplication unless an equivalent representative exists.

---

## Proof

### Step 1 — Parameterization of an inscribed square

Let \(P\) be a simple polygon with cyclically ordered edges. Let \(Q = (p_1,p_2,p_3,p_4)\) be a nondegenerate square inscribed in \(P\), with vertices listed in **forward boundary order** around \(P\).

Each \(p_k\) lies on some edge \(e_{i_k}\) of \(P\). Because the listing is in forward boundary order, the edge indices satisfy
\[
i_1, i_2, i_3, i_4
\]
in strict forward cyclic order, allowing repeats when multiple vertices lie on the same edge.

Write \(p_k = e_{i_k}(u_k)\) with \(u_k \in [0,1]\). If two vertices lie on the same edge, their parameters are strictly increasing in forward order.

There exists a side vector \(v = p_2 - p_1 \neq 0\) and a rotation \(J\) by \(\pm 90^\circ\) such that
\[
p_2 = p_1 + v,\quad p_3 = p_1 + v + Jv,\quad p_4 = p_1 + Jv.
\]
These are exactly the six scalar equations solved by the engine.

### Step 2 — Edge quadruple examined

The solver enumerates all 4-tuples \((i_1,i_2,i_3,i_4)\) in forward cyclic order, including repeated indices when geometrically valid (`PolygonCurve.iter_cyclic_edge_quadruples`).

For the quadruple attached to \(Q\), both \(J = +90^\circ\) and \(J = -90^\circ\) are attempted. One choice matches the cyclic labeling of \(Q\); that branch yields the correct linear system.

### Step 3 — Interior, endpoint, and repeated-edge cases

- **Interior vertices:** \(u_k \in (0,1)\) are direct feasible values.
- **Polygon vertices:** occur as \(u_k \in \{0,1\}\); still satisfy edge membership.
- **Vertex shared by two edges:** the square vertex may be assigned to either adjacent edge; at least one assignment yields a valid forward 4-tuple.
- **Multiple vertices on one edge:** repeated edge index with strictly increasing parameters is allowed by `_is_valid_edge_quadruple` and boundary-order checks.
- **Orientation of \(P\):** polygons are normalized to positive signed area before solving; reversal is tested separately in the test suite.

### Step 4 — Solution set, not samples

For the examined quadruple:

- Rank 6: the unique solution equals \((u_1,\ldots,u_4,v_x,v_y)\) for \(Q\).
- Rank 5: the solution set is an exact affine line \(x(t)=x_0+td\); feasibility is an exact union of parameter intervals. Isolated endpoint squares are emitted as exact certificates; the family itself is stored in `AffineSquareFamily1D` without sampling as the mathematical result.
- Rank \(\leq 4\): returned as `UnsupportedHigherDimensionalFamily` (not silently discarded).

### Step 5 — Deduplication

Certificates are deduplicated by canonical square-vertex key modulo dihedral symmetry. If two edge assignments produce the same geometric square, one representative suffices; the square is not lost.

---

## Assumptions

1. \(P\) is simple (validated at construction).
2. Coordinates are exact rationals for certified isolated squares.
3. Rank \(\leq 4\) positive-dimensional families are **not** yet fully certified for feasibility.

---

## Known gaps

- Completeness of feasibility for rank \(\leq 4\) families is **not** claimed.
- Floating-point polygons use interval status `unresolved`, not exact certificates.
- Deduplication identifies squares by vertex coordinates; distinct edge assignments of the same geometric square collapse to one entry (by design).
