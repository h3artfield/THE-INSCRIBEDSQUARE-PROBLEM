# Obstruction-Protected Bridge (T032‡)

## Statement — T032‡

If every compatible **obstruction-protected** square component along a polygonal sequence has persistence radius tending to zero, then an area-tight subsequence exists.

**Status:** `T032‡ — CONJECTURAL_FULL_BRIDGE`

## Relation to prior bridges

| Bridge | Status | Note |
|--------|--------|------|
| T032 (certificate) | **Withdrawn** (F014) | \(\rho^{\mathrm{cert}}\to0\) invalid |
| T032* | CONJECTURAL | Isolated intrinsic only |
| T032† | Superseded as primary | Used unproved family persistence |
| T032‡ | **Primary target** | Only admissible obstruction-protected components |

## Directive 017 impact

Circle family does not contribute to \(\rho_\square^{\mathrm{obs}}\) until T038-Curve or nonzero \(w_d(E)\) is proved.

Do **not** attempt T036-N nested-lobe bridge until a valid circle-family obstruction or proof that only isolated components matter in \(\mathcal D_{\mathrm{nest}}\).

Implementation: `obstruction_radius.py`.
