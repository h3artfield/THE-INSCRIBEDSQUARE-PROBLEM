# Marked Cyclic Gate Measures — Π_v (Directive 055)

## Mark space M_gate

Each gate carries:

- normalized boundary phase \(x \in S^1\);
- normalized parameter phase \(y \in S^1\);
- child state;
- geometric scale;
- normalized center;
- attachment increment;
- sign;
- parameter-component label;
- gate multiplicity.

Finite/countable gates form the marked measure

\[
\Pi_v = \sum_i q_i\,\delta_{m_i},
\]

with weights \(q_i\) from exact signature/transition data.

## Seam independence

Boundary and parameter order are cyclic. Representation uses anchored phases modulo rotation; `cyclic_gate_measure.audit_cyclic_gate_measure` verifies seam independence on the fixture.

## One-point limitation

\(\Pi_v\) alone does not determine traversal pairing, cross-wedge signs, collision multiplicity, or nonlocal interleaving — motivating \(\Omega_v\) and \(\Lambda_v\).

**Module:** `marked_gate_measure.py`, `cyclic_gate_measure.py`
