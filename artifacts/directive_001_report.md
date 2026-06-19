# Directive 001 Report — Rigorous Finite Foundation

**Date:** 2026-06-18  
**Status:** Complete — all acceptance tests pass (19/19)

---

## Implementation summary

Directive 001 established the local repository, theorem ledger, `PolygonCurve` data model, exact edge-quadruple square solver, `SquareCertificate` schema, independent floating-point oracle, and test suite.

| Component | Location |
|-----------|----------|
| Polygon model | `src/squarepeg/curves/polygon.py` |
| Exact solver | `src/squarepeg/exact_squares/solver.py` |
| Test oracle | `src/squarepeg/exact_squares/oracle.py` |
| Certificates | `src/squarepeg/certificates/schema.py` |
| Theorem ledger | `docs/theorem_ledger.md` |
| Tests | `tests/test_polygon.py`, `tests/test_square_solver.py` |

No adversarial optimization, Floer computation, or universal-conjecture claims were made.

---

## Solver mathematics

For polygon edges \(e_i(u_i) = a_i + u_i d_i\) with \(u_i \in [0,1]\), a square with side vector \(v\) satisfies:

\[
\begin{aligned}
e_2(u_2) &= e_1(u_1) + v \\
e_3(u_3) &= e_1(u_1) + v + Jv \\
e_4(u_4) &= e_1(u_1) + Jv
\end{aligned}
\]

where \(J\) is rotation by \(\pm 90^\circ\).

Rearranging gives **six linear equations** in \((u_1, u_2, u_3, u_4, v_x, v_y)\). For each cyclic edge quadruple and each rotation choice, the system is solved by exact Gaussian elimination over `Fraction` when coordinates are rational.

**Acceptance checks per candidate:**

1. All \(u_i \in [0,1]\)
2. Side length squared \(> 0\)
3. Vertices lie on claimed edges (collinearity + segment membership)
4. Cyclic boundary order (including repeated-edge parameter monotonicity)
5. Deduplication modulo cyclic relabeling and reversal of square vertices

**Rank-deficient systems:** rank \(< 5\) → `singular` certificate with matrix data; rank \(= 5\) → one-dimensional family with explicit `particular + t·direction` and sampled exact points.

---

## Complexity

For an \(n\)-edge polygon:

- Edge quadruples enumerated: \(O(n^4)\) with cyclic-order filtering (repeated edges allowed)
- Per quadruple: \(6 \times 6\) Gaussian elimination — \(O(1)\)
- Total: **\(O(n^4)\)** exact solves; practical for \(n \lesssim 20\) in interactive use

Memory: \(O(n)\) for polygon storage; certificates emitted per distinct square class.

---

## Tests and results

```
pytest tests/ -v  →  19 passed in ~109s
```

| Test area | Result |
|-----------|--------|
| Unit square, rectangle, triangle | Exact certificates found |
| Pentagons, random simple polygons | At least one square each |
| Interior-vertex squares (4×4) | Corner + midpoint (u=1/2) squares |
| Serialization / hash roundtrip | Stable |
| Similarity transforms | Count preserved within rational-rotation tolerance |
| Boundary reversal | Square count invariant |
| Oracle cross-check (3×3) | Exact count ≤ sampled oracle + margin |
| Singular / family systems | Reported, not silently discarded |

---

## Unsupported degeneracies

- **Self-intersecting polygons:** rejected at construction
- **Rank \(< 5\) positive-dimensional families beyond line:** reported as `singular`; not fully parametrized
- **Irrational rotations in transforms:** coordinates rounded via `limit_denominator`; may miss some exact solutions after rotation
- **Interval certificates:** schema supports `interval` type; implementation deferred
- **Oracle:** sampled boundary points only — can over-count; never used as certificate source

---

## Example emitted certificate

Unit square on `PolygonCurve([(0,0),(4,0),(4,4),(0,4)])`, midpoint square (vertices at edge midpoints):

```json
{
  "certificate_type": "exact",
  "cyclic_order_verified": true,
  "diagonal_length_squared": "16",
  "edge_indices": [0, 1, 2, 3],
  "edge_parameters": ["1/2", "1/2", "1/2", "1/2"],
  "orientation": "ccw",
  "polygon_hash": "b11e3248fe82779f19aca60385781e223a0e15bc0c99ffb3f15b71f51ccd04a1",
  "residuals": {
    "edge2": "(Fraction(0, 1), Fraction(0, 1))",
    "edge3": "(Fraction(0, 1), Fraction(0, 1))",
    "edge4": "(Fraction(0, 1), Fraction(0, 1))"
  },
  "side_length_squared": "8",
  "side_vector": ["2", "2"],
  "vertices": [["2", "0"], ["4", "2"], ["2", "4"], ["0", "2"]]
}
```

Family certificate (one-dimensional moduli on axis-aligned square):

```json
{
  "certificate_type": "family",
  "family_data": {
    "direction": ["1/4", "1/4", "1/4", "1/4", "-1", "1"],
    "free_param": "vy",
    "particular": ["0", "0", "0", "0", "4", "0"],
    "rank": 5
  },
  "edge_indices": [0, 1, 2, 3],
  "solve_rank": 5
}
```

---

## Theorem ledger updates

Initial entries added: T001–T008 (see `docs/theorem_ledger.md`).

| ID | Status |
|----|--------|
| T001 Toeplitz conjecture | CONJECTURE |
| T002 Noncollapse lemma | PROVED_LOCALLY |
| T003 Greene–Lobb derivative | SOURCE_THEOREM |
| T004 Midpoint extraction | PROVED_LOCALLY |
| T005 Midpoint nonflatness | CONJECTURE |
| T006 Asano–Ike square-angle target | CONJECTURE |
| T007 All polygons have squares | SOURCE_THEOREM |
| T008 Edge-quadruple linear reduction | PROVED_LOCALLY |

---

## Next recommended task

**Directive 002 (proposed):** Milestone 2 completion — interval-arithmetic certificate path, transformation-invariance stress tests on a fixed benchmark polygon set, and independent numerical comparison harness with timing/accuracy report.

Alternatively, begin **Milestone 3 functional LP** (Track 6) to test whether known spectral axioms imply midpoint nonflatness — this is high ROI before further theoretical work.

---

## Single most important unresolved issue

The exact polygon laboratory certifies **finite** squares; it does not address whether nested polygon sequences can force all square scales to zero while converging to a Jordan curve with flat spectral midpoint. That is the mathematical gap (T005), not a bug in the solver.
