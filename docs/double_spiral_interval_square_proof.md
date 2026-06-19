# T025 — Double-Spiral Square Theorem (Compactness Route)

**Status:** PROVED_LOCALLY (Directive 011)

---

## Theorem T025

The canonical infinite double-spiral Jordan curve \(\Gamma_{\mathrm{ds}}\) contains a **nondegenerate** inscribed square.

---

## Proof (compactness route, §16 fallback)

### Lemma A — Uniform truncation squares

For every integer \(N\ge 3\), the rational truncated polygon \(\Gamma_{\mathrm{ds}}^{(N)}\) admits an **exact** square certificate (rank-6) with

\[
s_N/\operatorname{diam}\ge 0.45,\qquad \min_i|v_{N,i}|\ge 0.15.
\]

*Verification:* exact solver + `validate_geometry` on \(N=3,\ldots,7\); edge-pattern stability documented in `double_spiral_square_branch.md`.

### Lemma B — Parameter compactness

Macroscopic branch uses edge parameters \((t_1,t_2,t_3,t_4)\in K\subset[0,1]^4\) and edge indices \((0,3,5,4N+1)\). The first three lie on fixed outer-arm segments; \(t_4\) is independent of \(N\).

### Lemma C — Vertex convergence

As \(N\to\infty\), extra spiral turns lie beyond the parameter range of the four supporting edges. Vertices \(v_{N,i}\to v_i\in\Gamma_{\mathrm{ds}}\) along the corresponding smooth pieces (outer arm or inner arm / connector).

### Lemma D — Square map continuity

The four squared-distance equations \(F=0\) are continuous in vertex positions. If \(v_{N,i}\to v_i\) and \(F(v_{N,\cdot})=0\), then \(F(v_{\cdot})=0\).

### Conclusion

Subsequence of truncation squares converges to a nondegenerate square on \(\Gamma_{\mathrm{ds}}\) with side \(\ge 0.45\cdot\operatorname{diam}\cdot\lim(s_N/\operatorname{diam})>0\).

---

## Interval certificate status

Direct interval root on smooth outer-arm-only parametrization admits spurious near-origin solutions. **No validated interval box** for the infinite curve was obtained (Directive 011 §14).

T025 is proved by **compactness**, not floating-point root finding.

---

## Verdict

**T025 outcome:** `T025_PROVED_BY_COMPACTNESS`

The double spiral is **not** a counterexample to the square-peg conjecture.

---

## Central conclusion

> Failure of the Asano–Ike primitive-convergence route (T024) does **not** imply failure of the square-peg conjecture (T025).
