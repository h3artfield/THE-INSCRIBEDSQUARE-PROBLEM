# Phase and Center Drift Falsification

**Directive 022 Part IX.**

## Phase-drifting towers

Rotate corridor phases by \(\Delta\phi\) per level. Fails `validate_coherent_tower` when \(\Delta\phi > C_{\mathrm{phase}} \lambda\).

Jordan property preserved; coherence destroyed.

## Center-drifting towers

Centers move by \(\approx 0.49 r_{j+1}\) per step. Cumulative drift can fail tower bounds; summable drift at threshold remains **insufficient** for cross-scale certificate.

## Branching towers

Two child packets in one parent invalidate single-tower comparison; requires tree-level invariant (T040 branch 3).

Module: `tower_falsification.py`.
