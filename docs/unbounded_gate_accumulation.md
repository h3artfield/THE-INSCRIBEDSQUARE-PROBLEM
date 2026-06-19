# Unbounded Gate Accumulation (Directive 029)

Separated from finite-tree topology.

## Residual classes

| Class | Condition |
|-------|-----------|
| UNBOUNDED_GATE_DENSITY_CLUSTER | \(\#\text{Gates}(C_n)\to\infty\) |
| DENSE_BOUNDARY_GATE_ACCUMULATION | Gates on shrinking boundary subarc |
| UNBOUNDED_OUTERPLANAR_BRANCHING | Branching count unbounded |
| NONVANISHING_JOIN_SIGNATURE_CLUSTER | Join signature dominates ear defect |

## Alternatives

Gate density forces: boundary subarc accumulation, unbounded branching, unbounded winding, positive scale, or join-signature dominance.

**Implementation.** `gate_accumulation.audit_gate_accumulation`.
