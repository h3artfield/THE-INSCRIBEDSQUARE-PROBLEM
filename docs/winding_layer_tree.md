# Winding Layer Tree (Directive 032)

Layer-cake identity:
\[
\int w_n^+ = \sum_{k\ge1}\operatorname{Area}\{w_n\ge k\}
\]

Domains \(E_{n,k}=\{x:w_n(x)\ge k\}\); \(E_{n,k+1}\subseteq E_{n,k}\).

**Winding-layer tree:** child at level \(k+1\) nested in parent at \(k\).

**Implementation.** `winding_layers.py`, `winding_layer_tree.py`
