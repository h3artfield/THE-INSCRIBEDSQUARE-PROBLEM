# Valid Polygon Square Families

## Re-audit (Directive 017)

Rank-5 nullity families from the exact solver are **not** automatically protected.

Each compact component requires:

| Field | Requirement |
|-------|-------------|
| Zero-set dimension | Actual \(d\), not rank alone |
| Tangent kernel | \(\ker DF = TZ\) verified |
| Cokernel rank | \(d = \dim\operatorname{coker}DF\) |
| Boundary | \(0\notin F(\partial U)\) |
| Collision margin | Positive |
| Obstruction | Nonzero \(\langle w_d(E),[Z]_2\rangle\) or proved curve restriction |
| Topology | Closed loop vs interval with endpoints |

Interval families with boundary are **not** automatically protected.

## Certificate

`ProtectedSquareFamilyCertificateV2` (`valid_family_certificate.py`) rejects rank-only certification.

Directive 016 `convert_family_to_protected` assigned `mod2_index_nonzero=True` without Euler computation — **withdrawn** for invariant purposes.
