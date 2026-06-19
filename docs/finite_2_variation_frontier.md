# Finite 2-Variation Frontier (T019)

**Gate status:** Part VIII **exploratory only** — Gate 1 (clean-room audit) **not passed**.

**Date:** 2026-06-18

---

## T019 — Conjectural target

> Every finite-(2)-variation Jordan curve admits regular \(C^1\) Jordan approximants \(S_n\to c\) uniformly whose Liouville primitives converge uniformly on compact subsets of the lifted parameter line.

**Status:** CONJECTURAL_TARGET

**Would imply:** Rectangular peg for finite 2-variation Jordan curves (via AI-PEG-v3 Thm 1.1).

---

## Why the \(p<2\) proof stops at \(q=2\)

Young pairing requires

\[
\frac{1}{p}+\frac{1}{q}>1.
\]

For primitive convergence we use **both** integrand and integrator in \(q\)-variation with the **same** exponent \(q\):

\[
\frac{1}{q}+\frac{1}{q}>1 \iff q<2.
\]

At \(q=2\): \(\frac12+\frac12=1\) — the inequality is **not strict**.

### Precise failure mode

| Issue | At \(q=2\) |
|-------|------------|
| Young existence for \(\int \xi\,dx\) when both paths are 2-variation | Borderline; log corrections may appear |
| Uniform bound \(\sup_t|f_n(t)-f(t)|\) via standard Young–Lœve | **Estimate fails** — no uniform constant from \(\|S_n-c\|_{2\text{-var}}\to 0\) alone |
| Uniqueness of limiting primitive from path alone | **Not established** |

**Do not say merely "Young doesn't work"** — the obstruction is **loss of strict integrability exponent** in the pairing bound used for **uniform** primitive convergence.

---

## Mechanism A — Lévy area

Study \(\mathbb A_n(s,t)=\frac12\int_s^t(x_n\,d\xi_n-\xi_n\,dx_n)\).

**Status:** Not investigated to conclusion. May require rough-path Lévy area convergence.

---

## Mechanism B — Winding-area primitive

Subarc + chord closure + winding. **Status:** Not proved independent of closing path at \(p=2\).

---

## Mechanism C — Conformal radial limits

\(c_r(t)=\phi(re^{it})\), \(f_r(t)=\int_0^t \xi_r\,dx_r\). **Status:** Boundary 2-variation does not automatically control \(r\to 1\) equicontinuity without extra hypothesis.

---

## Required outcome (Directive 007 §23)

**P2-E — Exact obstruction isolated**

The unresolved lemma is:

> **L-p=2 (Young pairing).** Find a replacement for the Young–Lœve bound at \(q=2\) that yields uniform convergence \(\sup_t|f_n(t)-f(t)|\) from \(\|S_n-c\|_{2\text{-var}}\to 0\) and uniform 2-variation bounds, **or** prove no such bound exists.

Until L-p=2 is resolved, T019 remains CONJECTURAL_TARGET.

---

## Do not proceed

- Arbitrary Jordan rough-path program  
- Full T019 proof attempt  
- Claiming \(p=2\) solved  

until Gate 1 passes and L-p=2 is addressed.
