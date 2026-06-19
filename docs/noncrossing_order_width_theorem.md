# Noncrossing Order-Width Theorem — T074R (Directive 038)

## T074R — Realizable unbounded-width reduction

If realizable gate permutations have monotone width tending to infinity, intrusion geometry must contain at least one of:

1. infinite nested intrusion ray;
2. unbounded branching;
3. disconnected parameter concentration;
4. non-Jordan saturation limit;
5. multicenter proliferation;
6. diffuse realizable permuton.

**Status.** `CONJECTURAL_STRUCTURAL_TARGET`; partial classifier via decreasing-subsequence geometry.

Decreasing gate subsequences are translated to reversed parameter/boundary intrusion arcs. Nested vs branching is estimated from LDS length and realizability audit.

**Implementation.** `intrusion_depth_from_order.py` (`certify_t074r_v2`)
