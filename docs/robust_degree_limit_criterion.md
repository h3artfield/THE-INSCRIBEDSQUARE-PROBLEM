# T031 — Positive Robust-Degree Limit Criterion

**Status:** `PROVED_LOCALLY`

---

## Statement

If \(P_n\to\gamma\) uniformly and there exist compatible fixed windows \(B\) with

\[
\limsup_{n\to\infty}\rho_\square^{\mathrm{cert}}(P_n,B)>0,
\]

and uniform boundary margins \(\inf_n m(\gamma_n,B)>0\) with uniform separation, then \(\gamma\) contains a nondegenerate inscribed square.

---

## Compatibility hypotheses (exact)

1. **Uniform convergence:** \(P_n\to\gamma\) in \(C^0\) (or uniform on \(S^1\)).
2. **Fixed windows:** Same ordered four-window box \(B\) for all \(n\) (or endpoints converge — moving-window version requires explicit endpoint convergence).
3. **Uniform boundary margin:** \(\inf_n m(\gamma_n,B)>0\).
4. **Uniform separation:** \(\inf_n d_{\min}(\gamma_n,B)>0\).
5. **Positive limsup robust radius:** \(\limsup_n\rho_\square^{\mathrm{cert}}(P_n,B)>0\).

---

## Proof sketch

For large \(n\), \(\rho_n>0\) gives protected box on \(P_n\) (T029). Uniform \(m>0\) and separation pass to limit. T030 on \(\gamma\) with inherited margin yields square on limit curve. Non-collapse via fixed side/separation bounds.

Implementation: `limit_persistence.py`.

---

## Moving-window variant

If \(B_n\to B\) with endpoint convergence and uniform \(\inf_n m(\gamma_n,B_n)>0\), same conclusion with additional hypothesis that window images converge in Hausdorff sense.

Not fully formalized in code — documented as extension.
