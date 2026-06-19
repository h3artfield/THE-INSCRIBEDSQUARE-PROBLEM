# T018 Variation Audit (Directive 007R)

**Result:** **Pass**

---

## 1-variation (§10)

\[
\mathrm{Var}_1(S-P;I_v)\le 2(|a|+|b|)\le 4r_v.
\]

Sum \(\sum_v 4r_v<\varepsilon\) achievable. **Valid.**

---

## q-variation (§11)

For \(q\ge 1\), on every partition \(\Pi\):

\[
\Bigl(\sum_i|\Delta h_i|^q\Bigr)^{1/q}\le\sum_i|\Delta h_i|
\]

since \((\sum x_i^q)^{1/q}\le\sum x_i\) for nonnegative \(x_i\) and \(q\ge 1\) (each term \(\le 1\) when normalized... standard: \(x^q\le x\) for \(x\in[0,1]\) doesn't apply; use: for \(a,b\ge 0\), \(a^q+b^q\le(a+b)^q\) when \(q\ge 1\)... 

Actually the directive proof: \((\sum|\Delta h_i|^q)^{1/q}\le\sum|\Delta h_i|\) because for each term, \(|\Delta h_i|^q\le|\Delta h_i|\) when \(|\Delta h_i|\le 1\)? That's wrong for large jumps.

Correct proof: For nonnegative \(x_i\), \(\|x\|_{\ell^q}\le\|x\|_{\ell^1}\) when \(q\ge 1\) because \(\ell^q\subset\ell^1\) for finite sequences with the convention that we compare \((\sum x_i^q)^{1/q}\) vs \(\sum x_i\).

Actually: \((\sum x_i^q)^{1/q} \le (\sum x_i)^{1/q} \cdot (\max?) \) 

Standard fact: For \(q\ge 1\), \(\|x\|_q \le \|x\|_1\) for \(x\ge 0\) in \(\mathbb R^n\). Proof: Hölder or Jensen: \(f(t)=t^q\) convex, ... 

Simplest: \(x_i^q \le x_i \cdot (\max_j x_j)^{q-1}\) - not uniform.

Correct: For \(q\ge 1\), \(t^q \le t \cdot s^{q-1}\) for \(0\le t\le s\)? If all \(x_i\le 1\), then \(x_i^q\le x_i\). For general: use that \(\|x\|_q \le \|x\|_1\) follows from power mean inequality: \((\frac{1}{n}\sum x_i^q)^{1/q} \le \frac{1}{n}\sum x_i\) when... 

Actually the directive's proof is: \((\sum|\Delta h_i|^q)^{1/q} \le \sum|\Delta h_i|\). 

Counterexample? Single term: \(|\Delta|^q \le |\Delta|\) iff \(|\Delta|\le 1\). Two terms: \(a=2, b=2\): lhs = (2^q+2^q)^{1/q} = 2\cdot 2^{1/q} > 4 = rhs? 

(2^q + 2^q)^{1/q} = 2 (2)^{1/q} < 4 for q>1. Good.

a=10, b=10: lhs = 10(2)^{1/q}, rhs=20. 10*1.26=12.6 < 20 for q=2. 

General: \((\sum x_i^q)^{1/q} \le \sum x_i\) for \(x_i\ge 0\), \(q\ge 1\). Proof: WLOG normalize... Actually use: for \(q\ge 1\), \(x^q \le x \cdot M^{q-1}\) where M = sum x_i, so sum x_i^q <= M^{q-1} sum x_i = M^q, so (sum x_i^q)^{1/q} <= M. Yes!

So \(|h|_{q\text{-var}}\le|h|_{1\text{-var}}\). **Pass.**

---

## Directive 007 error (F010)

Prior audit incorrectly flagged \(\|S-P\|_{q\text{-var}}\le\|S-P\|_{1\text{-var}}\) as false. **Retracted.**

Optional sharper route: oscillation interpolation inequality retained separately.
