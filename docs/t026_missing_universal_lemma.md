# T026 — Missing Universal Lemma

**Status:** `CONJECTURAL_FULL_BRIDGE` (unchanged)

---

## Unresolved assertion

> If a Jordan curve has **no** area-tight simple polygonal approximation sequence, then some four ordered compact parameter intervals carry a square map of **nonzero Brouwer degree**.

This is the precise missing step between T024-A (double-spiral area obstruction) and a universal square via degree (T026 branch 2).

---

## Why the double spiral supports the possibility

| Phenomenon | Evidence |
|------------|----------|
| Area-tight cyclic polygons fail | T024-A (`RESTRICTED_CLASS_ONLY`) |
| Protected outer degree box | T025/T027: \(\deg(F,B,0)=-1\) on four \(\gamma_+\) windows |
| Wild tail irrelevant | Square certified from four windows only; tail may be arbitrary (T028) |

The canonical double spiral is a **candidate** for branch (2): a macroscopic square with certified local degree, while area-tight approximants fail on the cyclic PL route.

---

## Why one example is not a proof

1. **Quantifier gap:** T024-A obstructs a specific PL interpolation class, not all area-tight sequences in the abstract.
2. **Degree is local:** T027 gives a square for curves \(C^0\)-close to four support pieces — not for every curve lacking area-tight approximants.
3. **No dichotomy mechanism:** Showing “no area-tight sequence \(\Rightarrow\) four-window degree configuration” requires a global topological or variational argument not present in Directive 013.
4. **T026 branch 1 unchanged:** T022 still handles the area-tight case; the bridge needs a theorem connecting failure of branch 1 to branch 2’s degree hypothesis.

---

## Refined T026 formulation (Directive 013)

Every Jordan curve either:

1. admits an area-tight simple polygonal approximation sequence (T022), **or**
2. contains a four-window configuration with **nonzero square-map Brouwer degree** (existence of square follows by degree).

Vague “macroscopic square directly” language replaced by the degree condition.

**Do not claim T026 proved.**
