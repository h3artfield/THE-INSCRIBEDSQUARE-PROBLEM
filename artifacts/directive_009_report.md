# Directive 009 Report — Jordan-Arc Area Control and T019

**Date:** 2026-06-18  
**Status:** COMPLETE

---

## Part I — T020 freeze

| Item | Status |
|------|--------|
| Manifest | `artifacts/t020_verified_release_manifest.json` |
| Tag | `t020-verified-release-2026-06-18` |
| Combined review | `review/T017_T020_combined_summary.md`, `T017_T020_dependency_map.pdf` |
| T017/T018/T020 code | Unmodified during T019 work |

---

## Part II–IV — T021

| Item | Result |
|------|--------|
| Relative signed area | Defined; equals chord-closed shoelace |
| Chord–lobe decomposition | Proved (general position + degenerate limits) |
| Constant | **`C = π/4 PROVED`** |
| Adversarial search | Max ratio ≈ π/8 (semicircle); all pass |

---

## Part V — Computational lab

`src/squarepeg/area_variation/` — exact DP 2-variation, certificates, adversarial generators.

---

## Part VI–VIII — T019 chain

| Step | Status |
|------|--------|
| ω_c superadditivity + continuity | Documented |
| Local PL 2-var control | \(C_0=1\) at nodes + limit |
| Primitive equicontinuity | T021 + coordinate bound |
| Arzelà–Ascoli subsequence | One sequence suffices |
| Adaptive T018 smoothing | Frozen template |
| Period lift + AI | Same as T017/T020 |

**No canonical Yang enhancement claimed.**

---

## Part X — Clean-room audit

`docs/t019_clean_room_audit.md` — all 10 questions **Yes**.

---

## Verdict

### Exactly one outcome

**Outcome A — T019 proved and audited**

```text
T019 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
T021 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
```

---

## Tests

164 passed (`python -m pytest tests/ -q`).

---

## Acceptance checklist

- [x] T020 frozen before T019 work
- [x] T021 proved (\(C=\pi/4\))
- [x] General-position + degenerate limit scheme
- [x] Exact polygonal 2-variation DP
- [x] Analytic primitive equicontinuity (not numerical proof)
- [x] One subsequence / no canonical enhancement
- [x] Adaptive smoothing for diverging length
- [x] Clean-room audit
- [x] Outcome A selected
- [x] Scope limited to finite 2-variation Jordan curves
