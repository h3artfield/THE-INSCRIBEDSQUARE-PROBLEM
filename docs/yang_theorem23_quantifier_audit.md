# Yang Theorem 23 — Quantifier Audit

**Source:** YANG-AREA-v1, Theorem 23 (statement page 9, proof page 36)  
**Status:** AUDIT COMPLETE (Directive 008R)

---

## Statement (Yang)

> Suppose \(\gamma\in C^{0,2-var}([0,T],V)\). Then \(\gamma\in G_2(V)\) **if and only if** \(A(\gamma^D)\) converges in **1-variation** as \(|D|\to 0\).

---

## What “as \(|D|\to 0\)” means in the proof

The proof of the \(\Rightarrow\) direction (page 36) uses **Lemma 45**: for refinements \(D_1\subset D_2\) with \(|D_1|,|D_2|\le\delta\),

\[
\|A(\gamma^{D_1})-A(\gamma^{D_2})\|_{1-var}\to 0\quad(\delta\to 0).
\]

For **general** partitions \(D,D'\) with \(|D|,|D'|\le\delta\), Yang sets \(D''=D\cup D'\) and applies the estimate twice (page 37, lines 1400–1401):

> For any finite partition \(D\) and \(D'\), denote \(D''=D\cup D'\), and use the above estimates for \(D,D''\) and \(D',D''\).

This is a **Cauchy family** in 1-variation over **all** finite partitions with mesh \(\le\delta\), not merely one selected sequence.

The \(\Leftarrow\) direction uses that limit to build a weak geometric 2-rough path; for vanishing 2-variation, geometric and weak coincide in the limit used.

---

## Contrast with Theorem 24

Theorem 24 (finite 2-variation) uses **existence of one sequence** \(\{D_n\}\) with equicontinuity — weaker hypothesis.

Theorem 23 is strictly about **vanishing** 2-variation and **full** partition convergence.

---

## Verdict

```text
ALL_PARTITIONS
```

Convergence as \(|D|\to 0\) means: the net \(\{A(\gamma^D):|D|\le\delta\}\) is Cauchy in 1-variation for every \(\delta\downarrow 0\), hence converges along **every** sequence of partitions with mesh tending to zero to the **same** limit \(\mathbb A_\gamma\).

---

## Load-bearing consequence for T020

Once \(\gamma\) is in the Theorem 33 modulus class, Theorem 33 proves this Cauchy property directly (page 38). **Any** partition family with mesh \(\to 0\) — including Boedihardjo–Geng partitions — yields the same area limit.
