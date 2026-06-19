# Yang Theorem 33 — Cauchy Estimate

**Source:** YANG-AREA-v1, proof page 38  
**Status:** REPRODUCED (Directive 008R)

---

## Modulus hypothesis (eq. (17))

Nondecreasing \(m:[0,1]\to\mathbb R_+\), \(m(t)\to 0\) as \(t\to 0\), \(\int_0^1 m(t)^2/t\,dt<\infty\), and

\[
\|\gamma(t)-\gamma(s)\|\le C|t-s|^{1/2}m(t-s).
\]

Then \(\omega_2(\gamma,\delta)\le Cm(\delta)\).

---

## Lemma 45 (refinement bound)

For \(D_2\) refining \(D_1\), \(|D_1|\le\delta\):

\[
\|A(\gamma^{D_1})-A(\gamma^{D_2})\|_{1-var}
\le \sum_k \|A(\gamma^{D_2})\|_{1-var,[t_k,t_{k+1}]}
+ 4\|\gamma\|_{2-var}\,\omega_2(\gamma,\delta).
\]

With \(\omega_2(\gamma,\delta)\le Cm(\delta)\) and \(\|\gamma\|_{2-var}\le C\):

\[
\le \sum_k \|A(\gamma^{D_2})\|_{1-var,[t_k,t_{k+1}]}+4C^2 m(\delta).
\]

---

## Inner bound (Lemma 47 + Thm 29 pattern, eq. (54) specialized)

Bisecting intervals as in Theorem 29 proof with \(p=q=2\), \(m_1=m_2=m\):

\[
\sum_k \|A(\gamma^{D_2})\|_{1-var,[t_k,t_{k+1}]}
\le 2C^2\Bigl(m(\delta)^2+2\int_0^\delta \frac{m(t)^2}{t}\,dt\Bigr).
\]

---

## Combined Cauchy estimate

For \(|D_1|,|D_2|\le\delta\), let \(D''=D_1\cup D_2\). Applying Lemma 45 twice (page 37):

\[
\|A(\gamma^{D_1})-A(\gamma^{D_2})\|_{1-var}
\le 2C^2\Bigl(2m(\delta)+m(\delta)^2+2\int_0^\delta\frac{m(t)^2}{t}\,dt\Bigr).
\]

**Repository form** (Directive 008R §4):

\[
\|A(\gamma^{D_1})-A(\gamma^{D_2})\|_{1-var}
\le C_1 m(\delta)^2 + C_2\int_0^\delta\frac{m(r)^2}{r}\,dr + C_3 m(\delta),
\]

with \(C_1=2C^2\), \(C_2=4C^2\), \(C_3=4C^2\) (constants absorbed in source's single bracket).

---

## Limit

As \(\delta\downarrow 0\): \(m(\delta)\to 0\) and \(\int_0^\delta m(t)^2/t\,dt\to 0\). Hence \(\{A(\gamma^D):|D|\le\delta\}\) is Cauchy in 1-variation.

By Theorem 23: \(\gamma\in G_2(V)\) with unique limit area \(\mathbb A_\gamma\).

---

## Implementation

`src/squarepeg/rough_area/yang_partition_area.py` — `theorem33_cauchy_bound`.
