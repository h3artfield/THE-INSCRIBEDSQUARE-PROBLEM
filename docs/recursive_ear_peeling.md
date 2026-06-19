# Recursive Ear Peeling (Directive 029)

## Algorithm

1. Find two-gate graph ear (leaf block or outermost chord);
2. Validate geometric ear when possible;
3. Mark for T051 surgery or remove from \(G_C\);
4. Resaturate remainder;
5. Repeat until two-gate remainder or irreducible graph.

Termination: \(\le |V|+|E|\) steps for bounded outerplanar graphs.

## Jordan preservation

Ordered surgery preserves injectivity when geometric ears validated; nested ears via maximal ancestor.

## Gate order

Peeling yields `GATE_ORDERED` forest when geometric gap absent; interleaving remains unprotected.

**Implementation.** `ear_peeling.peel_ears`.

**Confluence.** `EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING`.
