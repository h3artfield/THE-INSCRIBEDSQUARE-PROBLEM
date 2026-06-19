# T025 Certificate Replay (Directive 013)

**Verdict:** `T025_CERTIFICATE_REPLAYED`

---

## Summary

A clean-room verifier (`independent_t025_verifier.py`) reconstructs the canonical \(\gamma_+\) map and square equations without importing the primary certificate assembly, Jacobian module, Krawczyk implementation, or midpoint validator.

Interval backend: `iv_backend_v1.py` (outward-rounded float enclosures).

---

## Checks performed

| Step | Result |
|------|--------|
| Support-piece formulas | \(\gamma_+(\theta)=r(\theta)(\cos\theta,\sin\theta)\), \(r=(1+\theta)^{-1/2}\) |
| Parameter-box membership | Root in \(\operatorname{int}(B)\), each \(\theta_i\in J_i\) |
| Outward-rounded curve evaluation | Vertex intervals enclose true positions |
| Square equations \(F\) | All four components contain zero on \(B\) |
| Jacobian enclosure | \(\det DF(B)\subset[-2.5\times10^{-4},-3.1\times10^{-5}]\), excludes 0 |
| Krawczyk inclusion | \(K(B)\subseteq \operatorname{int}(B)\) |
| Side length | LB \(\ge 0.355\) |
| Distinct vertices | Pairwise separation LB \(\ge 0.335\) |
| Boundary order | \(\theta_1<\theta_4<\theta_2<\theta_3\) along outer arm |
| Origin exclusion | Radius LB \(\ge 0.248\) |

---

## Frozen artifacts

- `artifacts/t025_smooth_square_certificate.json`
- `artifacts/t025_verified_internal_manifest.json`
- Tag: `t025-smooth-double-spiral-internal-2026-06-18`

**Status label:** `T025 — PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE`

Not externally verified.
