# Local Area Change Under Surgery

**Directive 023 §7–§8.**

## Estimate

\[
\left|\mathcal A_{S_I(P)}(J) - \mathcal A_P(J)\right|
\le C_{\mathrm{area}} r^2 + C_{\mathrm{end}} r \cdot \operatorname{osc}(P;J)
\]

Straight chord: replacement arc has same endpoints \(\Rightarrow\) relative area change zero on \(J \subset I\); bound \(C r^2\).

Collar crosscut: \(|\mathcal A| \le C_{\mathrm{cross}} r^2\) with \(C_{\mathrm{cross}} = \pi/4\).

Implementation: `area_change.py`.

## Cases

Disjoint, subset, contains, one endpoint, seam — intervals outside \(I\) unchanged exactly.
