# Directive 007R Report — Repair T018 and Re-run Clean-Room Gate

**Date:** 2026-06-18  
**Status:** Complete  
**Verdict:** **Outcome A — Gate 1 passed**

---

## Summary

T018 repaired with **velocity-matched cubic Bézier** splices. T018-R2 audit finding **retracted** (F010). Lifted-period bound inserted. Clean-room re-audit passes.

```text
T017 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
T018 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
```

**Gate 1: PASSED.** Part VIII (\(p=2\)) not started (per directive).

---

## Part I — Audit record correction

| Item | Action |
|------|--------|
| T018-R2 | **Retracted** — \(\|h\|_{q\text{-var}}\le\|h\|_{1\text{-var}}\) valid |
| F010 | Erroneous audit finding logged |
| F009 | Closed — cubic repair |

---

## Part II–V — T018 repair

| Component | Status |
|-----------|--------|
| Cubic controls \(Q_0,\ldots,Q_3\) | Implemented |
| Endpoint velocity match | Proved |
| \(w\cdot S'>0\) injectivity | Proved |
| Global Jordan | Pass (disjoint disks) |
| \(\|S-P\|_{1\text{-var}}<\varepsilon\) | Pass |
| \(\|S-P\|_{q\text{-var}}<\varepsilon\) | Pass (monotonicity) |

**Code:** `src/squarepeg/variation/cubic_corner_smoothing.py`

---

## Part VI–VIII — T017 chain

BG \(\to\) cubic T018 \(\to\) Young \(\to\) period lift \(\to\) AI-PEG-v3 — **verified**.

---

## Tests

**121 fast tests passing** (new: cubic smoothing, norm monotonicity, period bound).

---

## Manuscript

Update `manuscript/finite_p_variation_rectangular_peg.tex` — audit-gap warning may be removed.

---

## Acceptance checklist

- [x] T018-R2 retracted in audit record
- [x] Cubic splice matches full velocity
- [x] Nonzero derivative / injectivity
- [x] Jordan embedding argument
- [x] Common parametrization explicit
- [x] 1- and q-variation estimates valid
- [x] Lifted-period estimate in proof
- [x] Clean-room re-audit complete
- [x] Outcome A selected
- [x] No \(p=2\) work started
