# T032 — Degree-Collapse-to-Area-Tightness Selection

**Status:** `CONJECTURAL_FULL_BRIDGE`

---

## Statement

Let \(\gamma\) be a Jordan curve and \(P_n\) cyclic simple polygonal interpolants with \(P_n\to\gamma\) uniformly.

If every subsequence with compatible protected boxes has \(\rho_\square^{\mathrm{cert}}\to0\), then some subsequence \(P_{n_k}\) is **area-tight**:

\[
\lim_{\delta\downarrow0}\limsup_{n\to\infty}\alpha_{P_n}(\delta)=0.
\]

---

## Area defect

\[
\alpha_P(\delta)=\sup_{d(s,t)\le\delta}|\mathcal A_P(s,t)|,
\qquad
\alpha_{(P_n)}(\delta)=\limsup_{n\to\infty}\alpha_{P_n}(\delta).
\]

---

## Dependency chain (if T032 true)

```text
T032 (degree collapse => area-tight subsequence)
  + T031 (positive limsup rho => square on limit)
  + T022 (area-tight => every rectangle)
=> square-peg conjecture
```

Branch split:

1. \(\limsup\rho_\square^{\mathrm{cert}}>0\) on some subsequence \(\Rightarrow\) square (T031);
2. otherwise T032 \(\Rightarrow\) area-tight subsequence \(\Rightarrow\) square (T022).

---

## Not proved in Directive 014

Counterexample search is diagnostic only. See `collapse_classifier.run_counterexample_search()`.

Missing lemma: `docs/t026_missing_universal_lemma.md` (updated for T032 formulation).
