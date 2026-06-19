# Obstruction-Protected Invariant

## Admissible protected components

\(\rho_\square^{\mathrm{obs}}(\gamma)\) includes **only**:

1. Isolated components with nonzero Brouwer degree
2. Morse-Bott components with proved nonzero \(w_d(E)\) pairing
3. Curve-restricted components with proved T038-Curve

## Removed from invariant

- Normal-index-only Morse-Bott components
- Rank-5 family certificates without Euler obstruction
- Provisional \(\rho_\square^{\mathrm{gen}}\) family contributions

## Definition

\[
\rho_\square^{\mathrm{obs}}(\gamma)=\sup\{\text{persistence radii over admissible components}\}.
\]

Isolated product-box radius remains a special case.

Implementation: `obstruction_radius.py`.

**Status:** \(\rho_\square^{\mathrm{gen}}\) is **not** mathematically valid as a persistence invariant without obstruction proof.
