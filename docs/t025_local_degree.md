# T025 Local Degree Certification

**Box:** \(B = J_1\times J_2\times J_3\times J_4\) with rational endpoints in `t025_frozen_constants.py` (radius \(3/20\) about certified root).

---

## Uniqueness

- Interval enclosure: \(0\in F(B)\) componentwise.
- Krawczyk operator: \(K(B)\subseteq \operatorname{int}(B)\).
- Midpoint residual \(|F(\theta^\*)|_\infty < 10^{-15}\) at discovered root.

Conclusion: exactly one zero of \(F\) in \(B\).

---

## Jacobian sign

Corner evaluation of \(\det DF\) on all \(2^4\) vertices of \(B\):

\[
\det DF(B)\subset[-2.496\times10^{-4},\ -3.073\times10^{-5}]
\]

Interval excludes zero. Constant sign:

\[
\operatorname{sgn}\det DF = -1 = \sigma
\]

---

## Brouwer degree

\[
\deg(F,B,0) = \sigma = -1 \ne 0
\]

Implementation: `square_boundary_degree.py`.

Degree inferred from certified nonsingular \(\det DF(B)\) and boundary exclusion — not from a single floating-point determinant.

---

## Module reference

| File | Role |
|------|------|
| `iv_backend_v1.py` | `det_interval_on_box` |
| `square_boundary_degree.py` | Degree certificate assembly |
| `artifacts/t025_boundary_exclusion_certificate.json` | Machine-readable record |
