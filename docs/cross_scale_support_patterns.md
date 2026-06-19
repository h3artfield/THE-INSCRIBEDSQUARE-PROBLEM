# Cross-Scale Support Patterns

**Directive 022 Part IV §9** — reconnaissance only.

## Patterns searched

| Pattern | Description |
|---------|-------------|
| OUTER_INNER_LEVELS | Vertices from gen 0 outer + gen k inner |
| NONADJACENT_LEVELS | gen 0 + gen k≥2 |
| FIXED_OUTER_WINDOWS | \(\theta \in \{0,\pi/2,\pi,3\pi/2\}\) at \(r_1\) |

Module: `cross_scale_rhombus.py`.

## Result

- **k=1:** geometric quadrilateral with side \(\approx 0.64 r_1\) (collision-free).
- **k≥2:** side \(\sim \lambda^k r_1\) collapses below \(0.12 r_1\).
- **No** \(w_1\)-certified cyclic-odd rhombus family on the full tower curve (T039 applies per packet only).

Fixed compact box \(U_{\mathrm{tower}}\): see `tower_cyclic_certificate.U_TOWER`.
