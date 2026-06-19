# Planar Inversion Extremal Bound (Directive 039)

## Crossing-number alternative

Auxiliary inversion graph: vertices = gates, edges = alternating-order pairs.

Under planarity, bounded depth \(D\), branching \(B\), and centers \(K\):

\[
\rho_{\mathrm{inv}} \le f(D,B,K), \qquad |E| \le \min(3n-6,\, DBKn/K).
\]

Superlinear edge count for diffuse rectangular mass yields contradiction with bounded geometry.

**Implementation.** `planar_inversion_graph.py`, `permuton_extremal_bound.py`
