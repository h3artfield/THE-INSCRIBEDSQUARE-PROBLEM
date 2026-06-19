# Computer-Assisted Proofs Inventory

| Result | Method | Independent replay |
|--------|--------|-------------------|
| T025 | Interval enclosure + Krawczyk | `iv_backend_v1`, `independent_t025_verifier` |
| T027 | Boundary degree + C⁰ homotopy | `c0_square_perturbation`, `square_boundary_degree` |
| T029–T031 | Abstract degree + perturbation | `robust_degree` package |
| Polygon exact | Rational linear algebra | `validator.py` independent of `equations.py` |
| T017–T021 | Analytic (frozen) | clean-room audits in release manifests |

**Not externally verified.**

Interval rounding: outward float enclosure (`iv_backend_v1`).

Polygon rank-6 \(\to\) protected box: `polygon_extractor` (computational lower bound on \(\rho_\square\)).
