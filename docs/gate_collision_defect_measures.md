# Gate Collision Defect Measures — Λ_v (Directive 055)

## Diagonal

\[
\Delta_{\mathrm{gate}} = \{(m,m'): x=x',\ y=y'\}.
\]

Weak limits may merge distinct gates to the same boundary/parameter location.

## Collision measure

\(\Lambda_v\) tracks mass approaching the diagonal as a weak-limit defect. Collision classes:

- HARMLESS_DUPLICATE_GATE
- RANK_MULTIPLICITY_COLLISION
- SHARED_GATE_DEGENERATION
- PARAMETER_COMPONENT_MERGER
- PINCHED_HULL_COLLISION
- NON_JORDAN_COLLISION

Diagonal mass is not discarded when wedge value vanishes.

## Routing

Nonharmless collisions route to shared-gate cluster analysis, parameter-disconnected support, non-Jordan degeneration, concentration, or named collision residual.

**Module:** `gate_collision_measure.py`
