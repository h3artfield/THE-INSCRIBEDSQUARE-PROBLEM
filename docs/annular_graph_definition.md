# ANNULAR_GRAPH — Quantitative Definition

**Directive 021.** Class \(\mathcal D_{\mathrm{nest}}^{\mathrm{ann}} = \mathcal D_{\mathrm{nest}} \cap \mathrm{ANNULAR\_GRAPH}\).

## Common center and polar graphs

For nested lobes \(L_1 \supset \cdots \supset L_m\), fix a center \(c \in \mathbb R^2\). Each selected boundary admits a polar radial graph

\[
\partial L_j = \{ c + r_j(\theta) e^{i\theta} : \theta \in S^1 \}
\]

outside attachment corridors, with \(r_j\) single-valued and continuous. Nesting alone does **not** imply star-shapedness.

Implementation: `src/squarepeg/defect_geometry/annular_graph.py`.

## Constants and geometric meaning

| Constant | Meaning |
|----------|---------|
| \(K \ge 1\) | Bounded eccentricity: \(\max_\theta r_j / \min_\theta r_j \le K\) on each selected layer |
| \(L \ge 0\) | Angular regularity: \(\|\log r_j(\theta)-\log r_j(\phi)\| \le L\, d_{S^1}(\theta,\phi)\) |
| \(g_- < g_+ < 1\) | Controlled radial gap: \(g_- \le r_{j+1}(\theta)/r_j(\theta) \le g_+\) away from corridors |
| \(w_{\mathrm{corr}}\) | Max total angular width (fraction of \(2\pi\)) of incoming/outgoing attachment corridors |
| \(\delta_{\mathrm{core}}\) | Core separation: \(r_j - r_{j+1} \ge \delta_{\mathrm{core}}\, d_{L_j}\) away from corridors |
| \(\zeta\) | Center drift: \(\|c_{j+1}-c_j\| \le \zeta\, d_{L_j}\) when layers use distinct centers |
| winding | All selected layers share orientation and winding sign |

## Membership

A normalized packet belongs to `ANNULAR_GRAPH` when the selected layer pair passes all checks in `validate_annular_graph()`.

## Certified regime (nonempty)

Directive 021 certifies:

- \(K = 1.005\)
- \(L = 0.01\)
- \(g_- = 0.449,\; g_+ = 0.451\)
- \(w_{\mathrm{corr}} = 0.005\)
- \(\delta_{\mathrm{core}} = 0.02\)
- \(\zeta = 0.002\)

Example packet: nearly circular ellipses with \(a/b = 1.005\) (`example_certified_packet()`).

## What this does not imply

- Unconditional T032§ for arbitrary Jordan limits
- Squares at fixed macroscopic scale when all packet outer diameters \(r_n \to 0\)
- Star-shapedness or radial-graph existence without the explicit hypotheses above
