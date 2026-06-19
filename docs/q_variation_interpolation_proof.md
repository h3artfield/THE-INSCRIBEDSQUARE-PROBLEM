# q-Variation Interpolation Inequality — Independent Proof

**Status:** PROVED_LOCALLY  
**Used in:** T017 polygonal step (supporting Lemma 3.1)

---

## Convention

\[
|u|_{r\text{-var};[a,b]}
=\left(\sup_{\Pi}\sum_i |u(t_{i+1})-u(t_i)|^r\right)^{1/r},
\qquad
\mathrm{osc}(u)=\sup_{s,t}|u(t)-u(s)|.
\]

Euclidean norm on \(\mathbb R^2\). Constant offsets are **not** included in the seminorm.

---

## Theorem (interpolation)

Let \(h:[a,b]\to\mathbb R^d\) have finite \(p\)-variation and finite oscillation. For \(0<p<q\):

\[
|h|_{q\text{-var}} \le \mathrm{osc}(h)^{1-p/q}\,|h|_{p\text{-var}}^{p/q}.
\]

**Best constant (this convention):** \(C_{p,q}=1\).

---

## Proof

For any partition \(\Pi=\{t_0<\cdots<t_n\}\), write \(\Delta_i h=h(t_{i+1})-h(t_i)\). Then

\[
|\Delta_i h|^q = |\Delta_i h|^{q-p}\,|\Delta_i h|^p
\le \Bigl(\max_j|\Delta_j h|\Bigr)^{q-p}|\Delta_i h|^p
\le \mathrm{osc}(h)^{q-p}\,|\Delta_i h|^p.
\]

Summing:

\[
\sum_i|\Delta_i h|^q \le \mathrm{osc}(h)^{q-p}\sum_i|\Delta_i h|^p.
\]

Taking \(\sup_{\Pi}\) and raising to \(1/q\):

\[
|h|_{q\text{-var}} \le \mathrm{osc}(h)^{(q-p)/q}\,|h|_{p\text{-var}}^{p/q}.
\]

Sharpness: single jump of size \(\mathrm{osc}(h)\) saturates the bound. ∎

---

## Application to \(P_n-c\)

If \(|P_n-c|_{p\text{-var}}\le C_p\) uniformly and \(P_n\to c\) uniformly, then \(\mathrm{osc}(P_n-c)\to 0\), hence

\[
|P_n-c|_{q\text{-var}} \le \mathrm{osc}(P_n-c)^{1-p/q} C_p^{p/q} \to 0.
\]

Combined with BG Lemma 3.1(2) (source) this gives the required polygonal \(q\)-variation convergence.

---

## Distinction from total variation

\(r=1\): rectifiability / length. For \(r>1\), finite \(r\)-variation does **not** imply rectifiability (Koch example, \(r>\log 4/\log 3\)).

---

## Reparametrization invariance

If \(\phi\) is increasing, then \(|u\circ\phi|_{r\text{-var}}=|u|_{r\text{-var}}\).  
**Warning:** invariance does **not** control \(|u\circ\phi - v\circ\psi|_{r\text{-var}}\) for unrelated reparametrizations — T018 uses a **common** parametrization.
