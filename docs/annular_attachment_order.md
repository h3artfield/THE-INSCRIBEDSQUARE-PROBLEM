# Annular Attachment Order

**Directive 026.**

`GATE_ORDERED`: maximal packets in parameter order have noninterleaving endpoint pairs.

Forbidden: A_i, A_j, B_i, B_j. Allowed: A_i, B_i, A_j, B_j (nested/separated).

Implementation: `annular_attachment_order.py`.
