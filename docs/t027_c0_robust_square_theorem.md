# T027 — Robust Double-Spiral Support Square Theorem

**Initial status:** `CONJECTURAL_TARGET`  
**Directive 013 status:** `T027_PROVED_LOCALLY_CLEAN_ROOM_VERIFIED`

---

## Statement

Let \(p_1,\ldots,p_4\) be the four canonical \(\gamma_+\) support pieces on certified intervals \(J_1,\ldots,J_4\).

There exists explicit \(\eta_0>0\) such that for any continuous maps \(q_i:J_i\to\mathbb R^2\) with

\[
\|q_i-p_i\|_\infty < \eta_0,
\]

the perturbed four pieces contain four distinct points forming a nondegenerate square in the same parameter boxes.

If the \(q_i\) are subarcs of a Jordan curve in cyclic boundary order, this yields an inscribed square on that curve.

---

## Proof ingredients (C⁰ only)

### Error bound

For \(|a'-a|,|b'-b|\le\eta\) and \(|a|,|b|\le R\):

\[
\bigl||a'-b'|^2-|a-b|^2\bigr| \le 8R\eta + 4\eta^2
\]

Each component of \(F\) is a difference of squared distances, hence

\[
\|F_q-F_p\|_{\infty;B} \le E(\eta) := 2\bigl(8R\eta+4\eta^2\bigr)
\]

with \(R\approx 0.423\) on support boxes (`c0_square_perturbation.py`).

### Certified radius

\[
\eta_0 \approx 1.1\times 10^{-5},\qquad E(\eta_0)\approx 7.5\times 10^{-5} < m\approx 9.0\times 10^{-5}.
\]

### Homotopy

\(F_\lambda=(1-\lambda)F_p+\lambda F_q\), \(0\le\lambda\le1\). On \(\partial B\):

\[
|F_\lambda|_\infty \ge m - E(\eta_0) > 0.
\]

Hence \(\deg(F_q,B,0)=\deg(F_p,B,0)=-1\ne0\), so \(F_q\) has a zero in \(B\).

### Nondegeneracy

\(d_{\min}\approx 0.335\) on \(B\); \(\eta_0\ll d_{\min}/4\). Side-length LB \(\ge 0.356\), radius LB \(\ge 0.248\) survive perturbation.

---

## What is not claimed

- Uniqueness after perturbation (existence only).
- Differentiability of perturbed pieces.
- Behavior outside the four support windows.

---

## Module

`src/squarepeg/residual_curves/c0_square_perturbation.py`
