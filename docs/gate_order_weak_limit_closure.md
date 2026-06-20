# Gate-Order Weak-Limit Closure (Directive 055)

Directive 054 isolated T105 failure: discrete `gate_order` is **NOT_CLOSED** under weak convergence while child-state measures and scalar coordinates converge.

## Information-loss audit

| Quantity | Status |
|----------|--------|
| BOUNDARY_ORDER_LOST | yes (without pair measure) |
| PARAMETER_ORDER_LOST | yes |
| CYCLIC_SEAM_AMBIGUITY | resolved by seam-independent representation |
| PAIRWISE_INVERSION_LOST | recovered by \(\Omega_v\) |
| CROSS_WEDGE_SIGN_LOST | recovered by \(\Omega_v\) |
| GATE_COLLISION_LOST | tracked by \(\Lambda_v\) |
| PARAMETER_COMPONENT_LOST | retained in marks |

## Functional closure audit

Under augmented moments on the fixture, gate-order functionals classify as WEAKLY_CONTINUOUS or REQUIRES_COLLISION_MEASURE; discrete `gate_order` eliminated.

**Fixture:** `data/regressions/gate_order_weak_closure_fixture.json`  
**Module:** `gate_measure_weak_closure.py`
