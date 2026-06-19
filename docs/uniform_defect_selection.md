# T037 — Uniform Defect Subsequence Dichotomy

**Status:** `PROVED_LOCALLY` (combinatorial)

---

## Statement

For nonnegative arrays \(a_{n,j}\) nonincreasing in \(j\), exactly one of:

**Alternative A:** exists \(n_k\to\infty\) with \(\lim_{j\to\infty}\limsup_k a_{n_k,j}=0\).

**Alternative B:** exists \(\varepsilon_0>0\) and infinite \(S\) such that for every fixed \(j\),
\(\liminf_{n\in S} a_{n,j}\ge\varepsilon_0\).

---

## Proof

Contrapositive: NOT B \(\Rightarrow\) A via nested infinite subsets with \(\varepsilon_m=2^{-m}\).

Implementation: `uniform_defect_selection.py`.

---

## Application

Closes T035-GAP: failure of area-tight subsequence \(\Rightarrow\) uniform persistent defect at every scale.
