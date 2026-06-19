# Canonical Intrusion Trees (Directive 040)

## Tree nodes

Rooted intrusion tree \(\mathcal T=(V,E)\). Each node records parameter subsystem \(I_v\), hull diameter \(r_v\), defect \(a_v\), gate count \(M_v\), centers, sign, parent/children, Jordan status, and gate class.

## Parent-child relation

Child \(w\) of \(v\) when parameter subsystem descends properly, image lies in \(H_v\), no intermediate separation, defect survives sibling removal. Relation is **order-independent**.

## Local finiteness

- `LOCALLY_FINITE_INTRUSION_TREE` — finitely many children per node
- `INFINITE_LOCAL_BRANCHING_TREE` — some node has infinitely many children

**Implementation.** `canonical_intrusion_tree.py`
