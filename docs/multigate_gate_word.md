# Multi-Gate Gate Word (Directive 029)

For saturated cluster \(C\) with gates \(g_1,\ldots,g_{2m}\) on \(\partial H(C)\):

## Gate word \(W(C)\)

Write gate labels in:
1. hull-boundary cyclic order;
2. parameter-circle order;
3. retained-curve exterior order.

## Pairings

Arcs inside \(H(C)\) are pairs \((g_i,g_j)\) tagged as:
- `SATURATED_INTERNAL`, `RETAINED_EXTERNAL`, `HULL_BOUNDARY`, `LOBE_CHORD`, `SURGERY_CROSSCUT`.

## Classification

| Kind | Meaning |
|------|---------|
| ADJACENT | Consecutive gates on parameter circle |
| NESTED | One arc contained in another |
| SEPARATED | Disjoint parameter intervals |
| ALTERNATING | Mixed nested/separated (not T039-protected) |

**Implementation.** `gate_word.build_gate_word`, `classify_pairings`.

Interleaving alone does **not** imply protected-square degree (T049).
