# Directive 007 Report — Clean-Room Audit and p=2 Frontier

**Date:** 2026-06-18  
**Status:** Complete  
**Verification verdict:** **Outcome B — Repairable gap**  
**p=2 frontier verdict:** **P2-E — Exact obstruction isolated** (exploratory; Gate 1 not passed)

---

## Part I — Freeze

- Manifest: `artifacts/t017_freeze_manifest.json`
- Frozen statement: `docs/t017_frozen_statement.md`
- Git commit: **none** (uncommitted working tree)
- Tests: **109 passed** (`pytest tests/ -m fast -q`)

---

## Part II–IV — Clean-room audit summary

| Component | Result |
|-----------|--------|
| BG polygonal interpolation | **Pass** |
| Interpolation inequality | **Pass** (C=1) |
| T018 common parametrization (variation) | **Pass** |
| T018 C¹ regularity | **Fail** — velocity mismatch at Bézier splices |
| T018 q-var from 1-var | **Fail** — false inequality; T018-R2 repair |
| Global Jordan embedding | Conditional pass |
| Young primitive (q<2) | Conditional pass |
| Lifted \(\mathbb R\) convergence | **Pass** with explicit bound |
| Koch / local monotonicity | **Corrected** — rectifiability only |

---

## Required repairs (before Outcome A)

1. **T018-R1:** Cubic Hermite (or equivalent) velocity-matched splices under common parametrization.
2. **T018-R2:** \(\|S-P\|_{q\text{-var}} \le \mathrm{osc}^{1-1/q}\|S-P\|_{1\text{-var}}^{1/q}\).
3. **T017-R1:** Insert explicit period-count bound in primitive proof.

---

## Part VI — Manuscript

- `manuscript/finite_p_variation_rectangular_peg.tex` — draft, audit-pending
- PDF: **not compiled** (pdflatex unavailable on freeze machine)

---

## Part VII — Verification verdict

**Outcome B — Repairable gap**

Ledger status:

```text
T017 — PROVED_LOCALLY_PENDING_CLEAN_ROOM_AUDIT
T018 — PROVED_LOCALLY_PENDING_CLEAN_ROOM_AUDIT
```

**Gate 1: NOT PASSED**

---

## Part VIII — p=2 (exploratory only)

**Why Young stops:** At \(q=2\), \(1/q+1/q=1\) — strict Young pairing fails for uniform primitive bounds.

**T019:** CONJECTURAL_TARGET

**P2-E:** Unresolved lemma **L-p=2** — replace Young–Lœve at \(q=2\) or prove obstruction.

No T019 proof attempted. Area anomaly constructions documented as heuristics only.

---

## Deliverables checklist

- [x] T017 independently reconstructed or downgraded → **Outcome B**
- [x] Common parametrization audited
- [x] Bézier splice velocities checked (not merely directions)
- [x] Global simplicity conditional pass
- [x] 1-variation bound independently derived
- [x] Lifted primitive convergence checked (explicit bound)
- [x] Koch citation corrected
- [x] Manuscript tex produced (PDF pending toolchain)
- [x] p=2 Young failure stated exactly
- [x] P2-E selected
- [x] No internal theorem marked externally accepted
