# T017 Clean-Room Audit (Re-run, Directive 007R)

**Date:** 2026-06-18  
**Prior verdict:** Outcome B (Directive 007)  
**Current verdict:** **Outcome A — Gate 1 passed**

---

## Reviewer checklist (§15)

| # | Question | Answer |
|---|----------|--------|
| 1 | Is \(S\) genuinely \(C^1\), not merely \(G^1\)? | **Yes** — cubic controls match full endpoint velocities \(u_\pm\) |
| 2 | Is \(S'\neq 0\) everywhere? | **Yes** — \(w\cdot dS/ds>0\) on each corner arc |
| 3 | Same parametrization for \(S-P\)? | **Yes** — `polygon_corner_sample` / common bridge segments |
| 4 | Globally embedded Jordan? | **Yes** — disjoint disk argument (small radii) |
| 5 | q-variation estimate? | **Yes** — \(\|S-P\|_{q\text{-var}}\le\|S-P\|_{1\text{-var}}\) (valid monotonicity) |
| 6 | Primitives converge on \(\mathbb R\)? | **Yes** — period-count bound inserted |
| 7 | Asano–Ike hypotheses met? | **Yes** — \(C^1\) + uniform primitive on compacts |

---

## Corrections from Directive 007

| Item | Resolution |
|------|------------|
| T018-R1 (velocity) | **Fixed** — cubic Bézier/Hermite (`docs/t018_velocity_matched_cubic.md`) |
| T018-R2 (q-var) | **Retracted as gap** — F010; inequality \(\|h\|_{q\text{-var}}\le\|h\|_{1\text{-var}}\) is valid |
| Lifted period | **Fixed** — explicit \(N_K\) bound in primitive proof |

---

## T017 chain (verified)

1. BG: simple PL \(P_n\), \(\|P_n-c\|_{q\text{-var}}\to 0\) — **imported, pass**
2. T018 (cubic): \(\|S_n-P_n\|_{q\text{-var}}\to 0\) — **pass**
3. Triangle: \(\|S_n-c\|_{q\text{-var}}\to 0\) — **pass**
4. Young: \(\sup|f_n-f|\to 0\) on period — **pass** (\(q<2\))
5. Lift: \(\sup_{[-K,K]}|f_n-f|\le\eta_n+N_K|I_n-I|\to 0\) — **pass**
6. AI-PEG-v3 Thm 1.1 + Remark 5.6 — **imported, pass**

---

## Status upgrade

```text
T017 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
T018 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
```

**Gate 1: PASSED**

---

## Imported vs local

| Component | Type |
|-----------|------|
| BG Thm 2.2, Lemma 3.1, Thm 3.1 | SOURCE |
| AI-PEG-v3 Thm 1.1, Remark 5.6 | SOURCE |
| Interpolation inequality (osc) | LOCAL |
| q-var monotonicity | LOCAL |
| T018 cubic smoothing | LOCAL (new) |
| Young primitive + period lift | LOCAL |
