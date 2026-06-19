# Jordan Gate Permutation Realizability (Directive 039)

## Finite Jordan gate system

A system consists of:

- Jordan disk \(H\);
- boundary gates \(g_1,\ldots,g_N\);
- finite embedded noncrossing intrusion arcs;
- parameter intervals;
- frozen boundary-order and parameter-order conventions.

The induced cyclic permutation \(\pi \in S_N / \text{cyclic shifts}\) is extracted via `encode_cyclic_order`.

## Realizability audit

Realizability is defined independently of implementation: outerplanar leaf gate graph + Jordan hull + noncrossing arcs.

Minimal topological data determining realizability: **noncrossing matching** (full intrusion tree when nonrealizable).

**Implementation.** `jordan_gate_realizability.py`
