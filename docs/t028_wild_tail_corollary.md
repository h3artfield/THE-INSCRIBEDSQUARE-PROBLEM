# T028 — Wild-Tail Stability Corollary

**Status:** `T028_PROVED_AS_COROLLARY` (conditional on T027)

---

## Statement

Let \(C:S^1\to\mathbb R^2\) be any Jordan curve. Suppose on four disjoint cyclic parameter intervals \(J_i\) its restrictions satisfy

\[
\|C|_{J_i}-p_i\|_\infty < \eta_0
\]

where \(p_i\) are the canonical double-spiral support pieces and \(\eta_0\approx 1.1\times 10^{-5}\).

No regularity assumption on the remainder of \(C\).

Then \(C\) contains a nondegenerate inscribed square.

---

## Allowed wild behavior elsewhere

The tail may have:

- infinite length;
- infinite 2-variation;
- nonrectifiable combs;
- nested spirals;
- failure of local monotonicity;
- failure of cyclic polygonal area-tightness (T024-A).

Requirements outside windows: continuity, injectivity, closure, correct cyclic attachment of the four subarcs.

---

## Examples (`wild_tail_examples.py`)

| Example | Modification | Jordan / pathology note |
|---------|--------------|-------------------------|
| `canonical_double_spiral` | Identity on windows | Reference curve |
| `modified_inner_exponent` | Inner arm exponent \(\alpha\ne1/2\) off-window | Nonstandard inner decay away from windows |
| `infinite_comb_tail` | Zigzag comb on connector only | Infinite 1-variation tail; bounded away from support \(\theta\) |

Square existence for each: invoke T027 on the four windows, not direct root finding.

---

## Proof chain

T027 (degree on \(B\)) \(\Rightarrow\) zero of perturbed square map \(\Rightarrow\) four distinct square vertices on \(C|_{J_i}\).
