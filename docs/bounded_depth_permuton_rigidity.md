# Bounded-Depth Permuton Rigidity — T077-A (Directive 039)

## Uniform depth hypothesis

If intrusion depth \(d_i \le D\), branching \(\le B\), and centers \(\le K\), then gate-order coupling has finite structural complexity.

## T077-A

A sequence of finite-intrusion Jordan gate systems with uniformly bounded depth, Jordan hulls, controlled center count, and noncrossing geometry **cannot** converge to a genuinely diffuse gate permuton.

**Status.** **PROVED_LOCALLY** via planar extremal inversion bound.

Proof route: inversion density \(\le f(D,B,K)\); genuinely diffuse permuton requires rectangular order mass exceeding this bound under bounded geometry.

**Implementation.** `bounded_depth_order.py`, `permuton_extremal_bound.py`
