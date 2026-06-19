# T024-B — No Primitive-Convergent \(C^1\) Approximation

**Status:** PROVED_LOCALLY under \(C^1\) convergence; OPEN for \(C^0\)-uniform only

---

## Target

No sequence \((Q_n)\) of regular \(C^1\) Jordan maps with \(Q_n\to\Gamma_{\mathrm{ds}}\) in \(C(S^1)\) and locally uniformly convergent normalized Liouville primitives \(f_n(0)=0\), \(f_n\to f\).

---

## Proved case (\(C^1\) uniform on \(S^1\))

Assume \(Q_n,\Gamma_{\mathrm{ds}}\in C^1(S^1,\mathbb R^2)\) and \(\|Q_n-\Gamma\|_{C^1}\to 0\).

Liouville identity (frozen convention):

\[
f_n(t)-f_n(s)=\frac{\xi_n(s)+\xi_n(t)}{2}\bigl(x_n(t)-x_n(s)\bigr)-\mathcal A_{Q_n}(s,t).
\]

On tail interval \(I_k=[u(M_k),u(N_k)]\):

1. **Endpoint term:** \(\|Q_n\|_\infty\) bounded, \(|x_n(t)-x_n(s)|\to 0\) since image \(\subset B(0,r(N_k))\), \(r(N_k)\to 0\). Hence chord term \(\to 0\) uniformly in \(n\) for fixed \(k\) large.

2. **Area term:** \(C^1\) convergence on the fixed angular range \([M_k,N_k]\) gives \(\mathcal A_{Q_n}(s_k,t_k)\to\mathcal A_\Gamma(s_k,t_k)\).

3. **Smooth lower bound:** \(|\mathcal A_\Gamma(s_k,t_k)|\ge c\log M_k-C\) (§5).

4. **Contradiction:** If \(f_n\to f\) uniformly, \(\{f_n\}\) is equicontinuous. For large \(k\), \(|t_k-s_k|\to 0\) but \(|f_n(t_k)-f_n(s_k)|\approx|\mathcal A_{Q_n}(s_k,t_k)|\ge c'\log M_k\to\infty\).

---

## Open case

If only \(Q_n\to\Gamma\) in \(C^0(S^1)\) without derivative control, relative area need not converge on shrinking intervals. **T024-B remains OPEN** in that generality.

---

## Verdict

| Statement | Status |
|-----------|--------|
| T024-B with \(\|Q_n-\Gamma\|_{C^1}\to 0\) | **PROVED** |
| T024-B with \(\|Q_n-\Gamma\|_\infty\to 0\) only | **OPEN** |

Do not conflate with T024-A.
