# Reference Annular Tower

**Directive 022 Part IV.**

## Construction

Self-similar tower with \(r_j = \lambda^j\), \(\lambda = 0.45\), common center, aligned corridors, star-annular geometry at each level.

Module: `reference_tower.py`.

## Jordan property

Finite truncations \(\Gamma^{(N)}\) are star-annular Jordan loops with inner cap at \(r_{N+1} = \lambda^{N+1}\).

Audit: `audit_reference_tower_jordan()` — injectivity (discrete), closed loop, annular certification at each level.

Infinite limit accumulates at \(c_\infty\) = tower center.

## Uniform convergence

\(\|\Gamma^{(N)} - \Gamma^{(\infty)}\|_\infty \lesssim r_N = \lambda^N \to 0\).
