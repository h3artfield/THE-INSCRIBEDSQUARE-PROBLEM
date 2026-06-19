# Nonrectifiable Examples

## Koch snowflake boundary

**Implementation:** `src/squarepeg/variation/self_similar_examples.py`

| Property | Value |
|----------|-------|
| Scaling ratio | 1/3 per segment |
| Length multiplier | 4/3 per iteration → ∞ |
| Hausdorff dimension | \(\log 4/\log 3\) |
| Finite \(p\)-variation | iff \(p>\log 4/\log 3\approx 1.262\) |
| Rectifiable | No (infinite length) |

**Minimum justified statement:** Finite \(p\)-variation class (for \(p<2\) suitable) is **strictly larger** than rectifiable curves.

**Not checked:** local monotonicity (Def. 5.10 / Prop. 5.11–5.12 — separate proof required).

**Do not cite** Prop. 5.9 for non-local-monotonicity (5.9 is rectifiability).

---

## Numerical note

`koch_p_variation(n,p)` on finite iterations is **exploratory**, not a proof of continuum variation.
