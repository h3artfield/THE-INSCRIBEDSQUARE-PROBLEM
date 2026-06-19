# Admissible Protected Invariant

## Definition

\[
\rho_\square^{\mathrm{adm}}(\gamma)
\]

= supremum of certified persistence radii over **admissible** components:

1. Isolated components with nonzero Brouwer degree
2. Morse-Bott components with nonzero \(w_d(E)\) (Euler obstruction)
3. **Cyclic-invariant rhombus continuation** with nontrivial diagonal sign-line pairing (T038-Curve)
4. Later independently proved curve-restricted components

## Removed

- Constant rank / normal degree alone
- Unproved \(\rho_\square^{\mathrm{gen}}\) family contributions
- Rank-5 polygon families without separate cyclic-odd or Euler audit

## Circle contribution

Unit circle family is admissible via **cyclic-odd** mechanism (`cyclic_odd_persistence.py`), not via Directive 017 cokernel line.

Implementation: `admissible_radius.py`.

Supersedes `docs/obstruction_protected_invariant.md` as primary formulation.
