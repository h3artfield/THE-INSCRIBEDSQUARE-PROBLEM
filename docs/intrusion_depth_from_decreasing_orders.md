# Intrusion Depth from Decreasing Orders (Directive 038)

Monotone-width duality: unbounded width \(\Leftrightarrow\) long decreasing gate subsequences.

A decreasing subsequence \(g_{i_1},\ldots,g_{i_k}\) yields intrusion arcs with reversed parameter/boundary order.

## Nested ray vs branching

If LDS length grows and arcs nest under Jordan noncrossing, compactness/König suggests an infinite intrusion ray.

If arcs do not nest, branching number grows or the saturation hull ceases to be Jordan.

This closes a major part of T074R at classifier level only.

**Implementation.** `intrusion_depth_from_order.py`
