# T036-N1-ANN — Annular-Graph Nested-Packet Square Theorem

**Status:** `PROVED_LOCALLY` (Directive 021)

## Statement (T036-N1-ANN)

Fix annular-graph constants in the certified regime (`CERTIFIED_REGIME` in `annular_graph_certificate.py`). Then every normalized packet in

\[
\mathcal D_{\mathrm{nest}}^{\mathrm{ann}}
\]

containing an appropriate separated pair of nested layers supports a cyclic-odd protected rhombus component. By T039, the packet contains a nondegenerate square with

\[
\operatorname{side}(Q) \ge c_{\mathrm{ann}}\, d_{L_j}, \qquad c_{\mathrm{ann}} = 0.12.
\]

## Proof chain

1. **ANNULAR_GRAPH** ⇒ radial graphs, gap control, corridor bounds (`validate_annular_graph`).
2. **Normalization** ⇒ common center, unit outer scale, median \(g_*\) (`normalize_layer_pair`).
3. **Comparison** ⇒ \(\Psi < \rho_{\mathrm{cyc}}\) in certified regime (`psi_from_constants`).
4. **Reference certificate** ⇒ T039 cyclic-odd component on \(\Gamma_{\mathrm{ref}}\) (`certify_reference_annular`).
5. **Persistence** ⇒ \(C^0\) closeness transfers protected component; diagonal defect crosses zero ⇒ square.

Audit: `certify_t036_n1_ann()` returns `t036_n1_ann_status='PROVED_LOCALLY'`.

## Depth required

**Two controlled layers suffice** (\(m_0 = 2\)). Depth is not used to force a layer pair beyond selecting outer/inner with separation \(q_0 \ge 1\).

## Scope

- **Proved:** packet-scale square at outer layer diameter scale.
- **Not proved:** universal T032§; shrinking packet squares without positive \(\limsup r_n\).
