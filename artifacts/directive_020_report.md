# Directive 020 Report

**Date:** 2026-06-18  
**Outcome:** **C — Missing geometric hypothesis identified**

---

## Summary

| Item | Result |
|------|--------|
| \(\mathcal D_{\mathrm{nest}}\) | Defined with quantitative constants |
| Reference \(\Gamma_{\mathrm{ref}}\) T039 | **Proved** (rank 3, \(w_1=1\), \(\rho_{\mathrm{cyc}}\approx0.01\)) |
| Window extraction | Algorithm + disjointness tests |
| T036-N1 unconditional | **Not proved** |
| T036-N1 conditional | If \(\Psi<\rho_{\mathrm{cyc}}\), T039 ⇒ square at outer scale |
| Missing hypothesis | **ANNULAR_GRAPH** (bounded eccentricity, corridor width) |
| T036-N2/N3 | CONJECTURAL |
| T032§ | Not attacked |

---

## Reference model (not Outcome D)

Star-annular curve carries valid cyclic-odd rhombus component. T039 applies.

---

## Why not Outcome A

Nesting + same-sign + scale separation do **not** imply \(\Psi < \rho_{\mathrm{cyc}}\). Eccentric ellipse falsification: nesting heuristics may hold; closeness fails.

---

## Strengthened class

\[
\mathcal D_{\mathrm{nest}}^{\mathrm{ann}}
=
\mathcal D_{\mathrm{nest}}
\cap \mathrm{ANNULAR\_GRAPH}
\]

---

## Scale distinction

T036-N1 (conditional) gives **local packet-scale** squares. Shrinking \(r_n\to0\) does not yield macroscopic limit squares without T036-N2 fixed-scale limsup.

---

**Tag:** `directive-020-nested-lobe-bridge-internal-2026-06-18`
