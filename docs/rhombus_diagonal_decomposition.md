# Rhombus–Diagonal Decomposition

For ordered parameters \(u=(u_1,\ldots,u_4)\), write \(p_i=\gamma(u_i)\) and \(s_i=|p_i-p_{i+1}|^2\).

**Rhombus map:**
\[
G_\gamma(u)=(s_1-s_2,\ s_2-s_3,\ s_3-s_4).
\]

**Diagonal defect:**
\[
D_\gamma(u)=|p_1-p_3|^2-|p_2-p_4|^2.
\]

**Square map:** \(F_\gamma=(G_\gamma,D_\gamma)\) in the frozen convention.

- \(G_\gamma=0\) ⇒ equal side lengths (rhombus away from collisions).
- \(G_\gamma=0\) and \(D_\gamma=0\) ⇒ nondegenerate square.

Implementation: `rhombus_map.py`.
