# Open Full Bridge — T032

---

## Conjecture (T032)

Robust-degree collapse on all compatible polygonal subsequences forces an area-tight subsequence.

---

## Why it matters

If T032 holds with T031 and T022:

```text
Every Jordan curve
  -> (limsup rho > 0) square by T031
  -> (else) area-tight subsequence by T032 -> square by T022
```

---

## Why it is open

1. Double spiral: area-tight fails (T024-A) but protected degree exists (T025/T027) — supports T026 branch 2, not T032.
2. T032 requires collapse on **all** compatible subsequences to force area-tightness — no proof from one example.
3. \(\rho_\square^{\mathrm{cert}}=0\) may be certificate failure, not collapse.
4. Rank-5 families block isolated degree assignment.

---

## First unresolved lemma (Directive 014 outcome E)

**T032-L1:** Prove or disprove that uniform convergence + degree-collapse on every compatible protected-window subsequence implies existence of an area-tight subsequence.

---

## Diagnostic program

`collapse_classifier.run_counterexample_search()` — numerical only.

Search for: \(\rho_\square^{\mathrm{cert}}\to0\) without area-tight subsequence.

---

## Related

- T026: dichotomy formulation
- T033: finite-scale prototype
- `docs/degree_collapse_blowups.md`: local rescaling analysis
