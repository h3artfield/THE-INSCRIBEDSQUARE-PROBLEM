# Finite 2-Variation Primitive Compactness

**Status:** PROVED_LOCALLY (Directive 009)

---

## Polygon primitives

\(f_n(t)=\int_0^t\xi_n\,dx_n\), \(f_n(0)=0\).

Identity (008R audited):

\[
f_n(t)-f_n(s)=\frac{\xi_n(s)+\xi_n(t)}{2}(x_n(t)-x_n(s))-\mathcal A_{P_n}(s,t).
\]

---

## Equicontinuity

Uniform bound \(|\xi_n|\le M\) from \(P_n\to c\) uniformly.

T021 + local interpolation:

\[
|f_n(t)-f_n(s)|\le M|x_n(t)-x_n(s)|+\frac\pi4\,\omega_c\bigl((s-\mu_n)_+,(t+\mu_n)_-\bigr).
\]

Right side \(\to 0\) as \(|t-s|\to 0\) uniformly in \(n\).

---

## Arzelà–Ascoli

\(\{f_n\}\) equicontinuous and bounded on \([0,1]\). Extract \(f_{n_k}\to f\) uniformly.

**Note:** Different subsequences may yield different \(f\); Asano–Ike requires only **one** approximating sequence.

---

## Smoothing + lift

Adaptive T018 (frozen) on selected \(P_k\); period lift as T017/T020 template.

---

## No canonical enhancement

This route does **not** claim Yang area convergence along all partitions — only compactness of one primitive subsequence.
