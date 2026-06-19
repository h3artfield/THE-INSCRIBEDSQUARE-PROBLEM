# Koch Snowflake — Local Monotonicity Status

**Date:** 2026-06-18  
**Directive 007 correction**

---

## AI-PEG-v3 organization (correct citation)

| Result | Content |
|--------|---------|
| **Proposition 5.8 / Corollary 5.9** | Rectifiable curves satisfy Theorem 1.1 |
| **Proposition 5.11 / Corollary 5.12** | Locally monotone curves satisfy Theorem 1.1 |
| **Definition 5.10** | Local monotonicity |

**Do not** cite Prop 5.9 as the "non-local-monotonicity" result — 5.9 concerns **rectifiability**.

---

## Koch snowflake

| Property | Status |
|----------|--------|
| Nonrectifiable | **Proved** (length \(\to\infty\)) |
| Finite \(p\)-var for \(p>\log 4/\log 3\) | Standard (Hausdorff dimension) |
| Not locally monotone | **Not proved in this repository** |

---

## Local monotonicity proof — not completed

To show Koch is **not** locally monotone (Def. 5.10), one must prove: at some boundary point, every neighborhood contains direction reversals for **every** candidate projection direction.

**This proof is not completed here.**

---

## Justified enlargement statement

> The finite-\(p\)-variation class (\(1\le p<2\)) is **strictly larger than the rectifiable class**.

**Evidence:** Koch snowflake with \(p\in(\log 4/\log 3, 2)\).

**Not claimed without proof:** Koch lies outside the locally monotone class.

---

## Action

Removed incorrect Prop 5.9 citation from novelty/enlargement claims. See `docs/t017_novelty_audit.md` (to be updated).
