# Geometric Ear Peeling (Directive 030)

Canonical order:
1. weak-dual leaves;
2. leaf blocks;
3. smallest hull diameter;
4. parameter tie-break.

Complexity \(\kappa(C)=|V|+|E|+\#\text{intrusions}\) strictly decreases each step.

Extracted ears form disjoint/nested cluster forest compatible with T051/T052.

**Implementation.** `geometric_ear_peeling.geometric_ear_peeling`.

**Status.** PROVED_LOCALLY.
