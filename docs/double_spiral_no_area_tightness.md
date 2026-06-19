# T024-A — No Area-Tight Cyclic Polygon Sequence

**Status:** PROVED_LOCALLY (Directive 011)

---

## Theorem T024-A

No sequence \((P_n)\) of simple polygonal interpolants with vertices in **cyclic parameter order**, converging uniformly to the canonical \(\Gamma_{\mathrm{ds}}\), is area-tight.

---

## Proof

### Step 1 — Shrinking tail intervals

Fix \(M_k\to\infty\), \(N_k=M_k^2\). On the outer arm, define parameter interval \(I_k=[u(M_k),u(N_k)]\) using the frozen inverse-radial parametrization. Then \(|I_k|\to 0\) and \(\mathrm{diam}(\gamma_+(I_k))\to 0\).

### Step 2 — Relative area lower bound (smooth)

For the smooth outer arm (Directive 011 §5):

\[
\frac12\int_{M_k}^{N_k}r(\theta)^2\,d\theta
=\frac12\log\frac{1+N_k}{1+M_k}
\ge\frac12\log M_k - O(1).
\]

Endpoint chord correction satisfies \(|C_k|\le r(M_k)r(N_k)\le (1+M_k)^{-1}=o(1)\). Hence

\[
\bigl|\mathcal A_{\gamma_+}(M_k,N_k)\bigr|\ge c\log M_k-C
\]

for explicit \(c=1/2\), \(C<\infty\).

### Step 3 — Polygonal transfer

Let \(P_n\to\Gamma_{\mathrm{ds}}\) uniformly with cyclic vertices. For each \(k\), choose \(n_k\) large enough that:

1. mesh on \([M_k,N_k]\) is smaller than a fixed \(\delta_k\);
2. Hausdorff distance \(<\min_j\delta_j(A_j')\) on each protected annulus \(A_j'\) with \(j\le k\) (winding stability);
3. polygonal relative area on the vertex chain between the two vertices closest to \(\gamma_+(M_k)\) and \(\gamma_+(N_k)\) differs from the smooth value by \(<1/2\cdot (c\log M_k-C)\) (Riemann-sum convergence of the antisymmetric form on a fixed angular interval).

Then

\[
\bigl|\mathcal A_{P_{n_k}}(s_k,t_k)\bigr|\ge\frac12(c\log M_k-C)>0
\]

while \(d_{S^1}(s_k,t_k)=|I_k|\to 0\). This contradicts area-tightness.

---

## Verdict

**T024-A: PROVED**

Area-tightness is **false** for the canonical double spiral (T023 refuted for this curve).

---

## Not claimed

Failure of **all** approximant types; T024-B is separate.
