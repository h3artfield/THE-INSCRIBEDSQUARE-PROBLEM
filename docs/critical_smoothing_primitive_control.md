# Critical Smoothing Primitive Control

**Status:** OPEN (blocks T020 Outcome A)

---

## Issue

For \(p=2\), T018 gives \(\|S_n-P_n\|_{1\text{-var}}<\varepsilon_n\) but **does not** control:

\[
\sup_t\left|\int_0^t\xi_{S_n}\,dx_{S_n}-\int_0^t\xi_{P_n}\,dx_{P_n}\right|
\]

when \(P_n\) has **growing** 1-variation (polygonal length \(\to\infty\) possible while 2-var vanishes).

---

## Required tolerance (§14)

Choose \(\varepsilon_n\) depending on:

- \(\|P_n\|_{1\text{-var}}\) (may grow);
- \(\|P_n\|_\infty\);
- target primitive error \(2^{-n}\);
- second-level convergence error from Yang estimate.

At \(q=2\), Young decomposition **fails** — must use enhanced area estimates (Yang Thm 29).

---

## Status

Not closed in Directive 008. Contributes to **Outcome B**.
