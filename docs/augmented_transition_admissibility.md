# Augmented Transition Admissibility (Directive 056)

## Class T_aug

Geometrically realizable or limit-realizable data \((X,\mathsf K,\Pi,\Omega,\Lambda,E,\Gamma)\).

Realizability classes:

| Class | Status |
|-------|--------|
| FINITE_REALIZABLE | included |
| COUNTABLE_REALIZABLE | included |
| MEASURE_REALIZABLE | included |
| LIMIT_REALIZABLE | included |
| ALGEBRAIC_ONLY | **excluded** |

## Consistency conditions

1. **Child-state consistency** — child marginal agrees with \(\mathsf K\).
2. **Gate marginal consistency** — one-point marginals of \(\Omega\) agree with \(\Pi\) modulo recorded multiplicity.
3. **Collision consistency** — diagonal mass missing from \(\Omega\) appears in \(\Lambda\).
4. **Exact state recursion** — every coordinate reconstructible from \((\mathsf K,\Pi,\Omega,\Lambda,E,\Gamma)\).
5. **Jordan compatibility** — compatible hull geometry or allowed limit degeneration.
6. **Parameter compatibility** — boundary and parameter cyclic-order data mutually realizable.

**Module:** `augmented_order_transition.py`, `gate_order_realizability.py`
