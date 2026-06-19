# Young Primitive Convergence — Proof

**Status:** PROVED_LOCALLY  
**Convention:** AI-PEG-v3 Liouville form \(\lambda=\xi\,dx\), \(c=(x,\xi)\).

---

## Setup

Let \(c:[0,1]\to\mathbb R^2\) be Jordan with finite \(p\)-variation, \(1\le p<2\). Fix \(p<q<2\).

BG Lemma 3.1 + T018 give \(C^1\) Jordan \(S_n\) with \(S_n\to c\) uniformly and \(\|S_n-c\|_{q\text{-var}}\to 0\) on a common parametrization.

Write \(S_n=(x_n,\xi_n)\), \(c=(x,\xi)\). Define

\[
f_n(t)=\int_0^t \xi_n\,dx_n,\qquad f(t)=\int_0^t \xi\,dx
\]

(Young integrals; classical for smooth \(S_n\)).

Normalize \(f_n(0)=f(0)=0\).

---

## Young estimate (BG Theorem 3.1 template)

For \(q<2\), \(1/q+1/q>1\). For any \(0\le s\le t\le 1\):

\[
\int_s^t \xi_n\,dx_n - \int_s^t \xi\,dx
= \int_s^t (\xi_n-\xi)\,dx_n + \int_s^t \xi\,d(x_n-x).
\]

As in BG proof of Theorem 3.2 (lines using Theorem 3.1):

\[
\left|\int_s^t (\xi_n-\xi)\,dx_n\right|
\le 2\zeta(2/q)\,\|\xi_n-\xi\|_{q\text{-var}}\,\|x_n\|_{q\text{-var}},
\]

\[
\left|\int_s^t \xi\,d(x_n-x)\right|
\le 2\zeta(2/q)\,\|\xi\|_{q\text{-var}}\,\|x_n-x\|_{q\text{-var}}.
\]

Coordinate \(q\)-variations are bounded by \(\|S_n-c\|_{q\text{-var}}\) and \(\|S_n\|_{q\text{-var}}+\|c\|_{q\text{-var}}\).

Hence

\[
\sup_{t\in[0,1]}|f_n(t)-f(t)| \le C_q\,\|S_n-c\|_{q\text{-var}} \to 0.
\]

---

## Closed integral and area

\[
I_n=\oint_{S_n}\xi_n\,dx_n = f_n(1)-f_n(0).
\]

Same bound gives \(I_n\to I=\oint \xi\,dx\).

Under AI-PEG-v3 orientation, \(I\) equals **signed enclosed area** (Green / BG Theorem 3.2 with \(f=0\), \(g=-x\) or equivalent — audit confirms sign in `docs/t017_independent_audit.md`).

---

## Lift to \(\mathbb R\)

For \(t\in[-K,K]\), write \(t=2\pi k+s\) with \(s\in[0,2\pi)\), \(|k|\le N_K:=\lceil K/(2\pi)\rceil+1\).

\[
|f_n(t)-f(t)| \le \eta_n + N_K|I_n-I|,
\]

where \(\eta_n=\sup_{[0,2\pi]}|f_n-f|\) and \(I_n=f_n(2\pi)\), \(I=f(2\pi)\).

Therefore

\[
\sup_{|t|\le K}|f_n(t)-f(t)| \le \eta_n + N_K|I_n-I| \to 0.
\]

**Do not use** "periodicity implies compact convergence" without this bound.

---

## Area normalization (AI-PEG-v3)

If \(A(S_n)\to A(c)\), scale \(\widetilde S_n=\sqrt{\pi/A(S_n)}\,S_n\) about the origin. Scaling by \(\lambda\):

- Jordan / \(C^1\) preserved;
- \(\|\widetilde S_n-S_n\|_{q\text{-var}}=|\lambda-1|\|S_n\|_{q\text{-var}}\to 0\);
- Primitive scales: \(\widetilde f_n=\lambda^2 f_n\) (since \(\xi\,dx\) scales by \(\lambda^2\) on \((\lambda x,\lambda\xi)\)).

After normalization, enclosed area \(=\pi\) and primitives converge uniformly.

---

## Implementation

`young_integral.py` — trapezoid on PL graphs validates formulas only.

Primary justification: **this document**.
