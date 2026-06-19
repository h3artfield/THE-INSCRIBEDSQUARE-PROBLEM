# Saturated Gate Graph (Directive 029)

## Definition

\(G_C\): vertices = gates; edges = connected saturated curve arcs inside \(H(C)\), embedded in the Jordan disk.

Edge kinds: `SATURATED_ARC`, `RETAINED_ARC`, `HULL_BOUNDARY`, `DEGENERATE`.

Multiple edges and degree \(>2\) tracked explicitly.

**Implementation.** `gate_graph.build_gate_graph`.

## T055 — Outerplanarity

For noncrossing chord embeddings with all gates on \(\partial H(C)\), \(G_C\) is **outerplanar**.

**Status.** PROVED_LOCALLY (`outerplanar_structure.audit_outerplanarity`).

Counterexample search: crossing chord pairs => `DISPROVED_COUNTEREXAMPLE`.
