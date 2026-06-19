# Area-Tight Subsequence Selection (T035)

**Status:** `PROVED_LOCALLY`

---

## T035 — Area-tight subsequence criterion

Subsequence \((P_{n_k})\) is area-tight iff

\[
\lim_{\delta\downarrow 0}\limsup_{k\to\infty}\alpha_{n_k}(\delta)=0.
\]

---

## Diagonal equivalent (\(\delta_j=2^{-j}\))

Constructive form: exists increasing \(n_k\) such that

\[
\alpha_{n_k}(2^{-j})<2^{-j}\quad\text{for all }j\le k.
\]

---

## Negation (quantifier audit)

**NOT** area-tight means: for every increasing \((n_k)\), exists \(j\) with \(\limsup_k\alpha_{n_k}(2^{-j})>0\).

**Does not imply** \(\alpha_n(\delta_j)\ge\varepsilon\) for all large \(n\) at one fixed \(j\). Defect may **migrate among scales**.

Implementation: `area_tight_selection.py`.
