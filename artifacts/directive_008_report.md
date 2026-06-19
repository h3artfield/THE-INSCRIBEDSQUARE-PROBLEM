# Directive 008 Report — Publication Lock and Critical-Modulus (p=2) Bridge

**Date:** 2026-06-18  
**Status:** COMPLETE

---

## Part I — T017/T018 publication lock

| Item | Status |
|------|--------|
| Release manifest | `artifacts/t017_verified_release_manifest.json` |
| Git tag | `t017-verified-release-2026-06-18` |
| Manuscript PDF | `manuscript/finite_p_variation_rectangular_peg.pdf` (tectonic 0.15.0) |
| Review packet | `review/T017_*` |
| External submission | **Not authorized** |

**T017/T018:** `PROVED_LOCALLY_CLEAN_ROOM_VERIFIED` — frozen.

**Tests at freeze:** 130 passed (`python -m pytest tests/ -q`).

---

## Part II — Critical exponent framing

| File | Content |
|------|---------|
| `docs/critical_young_source_ledger.md` | YANG-AREA-v1 pinned; Thm 33, modulus condition, counterexamples |
| `docs/critical_variation_class_hierarchy.md` | Classes A–D; valid/failed implications |
| `docs/area_enhancement_dependency_graph.md` | Dependency graph |

**Key separation:** vanishing 2-variation **does not** imply enhancible (Yang).

---

## Part III–VI — T020 program

| Step | Result |
|------|--------|
| T020 stated | `docs/critical_modulus_rectangular_peg.md` |
| Vanishing 2-var from modulus | Proved (sublemma §8) |
| Yang critical Young / G₂ | Imported (Thm 33); estimate in ledger |
| Rough → Liouville | `docs/rough_area_to_liouville_primitive.md` |
| BG polygon → G₂ enhancement | **UNRESOLVED** (`docs/simple_polygon_rough_convergence.md`) |
| T018 adaptive smoothing at p=2 | Blocked pending polygon enhancement (`docs/critical_smoothing_primitive_control.md`) |

**Code (exploratory, not proof):** `src/squarepeg/rough_area/`

---

## Part VII — Exact-critical examples

`docs/exact_critical_examples.md` — candidate modulus \(m(r)=(\log(e/r))^{-\alpha}\), \(\alpha>1/2\).  
Jordan injectivity and failure of finite \(p\)-var for all \(p<2\) **not fully closed**.  
Claim limited: T020 extends finite-\(p<2\) theorem, not every prior class.

---

## Part VIII — T019 stress test

`docs/finite_2_variation_counterexample_program.md`

**T019 status:** **STILL OPEN**

- Yang paths with area anomaly exist (non-Jordan).
- No planar Jordan construction preserving anomaly completed.
- One bad approximation sequence does **not** disprove T019.

---

## Required verdicts

### T020 — exactly one outcome

**Outcome B — Polygonal enhancement mismatch**

Critical-modulus paths receive \(\mathcal G_2\) enhancement (Yang Thm 33), but Boedihardjo–Geng simple Jordan interpolants are **not shown** to converge to that enhancement in the topology required for Asano–Ike primitive convergence.

### T019 — separate classification

**STILL OPEN**

---

## Acceptance checklist

- [x] T017/T018 frozen and compiled
- [x] No external acceptance claimed
- [x] Finite / vanishing / enhancible classes separated
- [x] Critical modulus stated exactly
- [x] Rough second level → Liouville documented
- [x] BG simple polygons analyzed (UNRESOLVED)
- [x] Smoothing tolerances documented (blocked)
- [x] T020 Outcome B selected
- [x] T019 separately classified
- [x] No numerical area convergence presented as proof

---

## Files created (Directive 008)

```
artifacts/t017_verified_release_manifest.json
artifacts/directive_008_report.md
docs/critical_young_source_ledger.md
docs/critical_variation_class_hierarchy.md
docs/critical_modulus_rectangular_peg.md
docs/area_enhancement_dependency_graph.md
docs/rough_area_to_liouville_primitive.md
docs/simple_polygon_rough_convergence.md
docs/critical_smoothing_primitive_control.md
docs/exact_critical_examples.md
docs/finite_2_variation_counterexample_program.md
review/T017_one_page_summary.md
review/T017_dependency_map.pdf
review/T017_proof_checklist.md
review/T017_author_query.md
src/squarepeg/rough_area/*.py
tests/test_critical_modulus.py
tests/test_second_level_identities.py
tests/test_primitive_recovery.py
tests/test_polygonal_lift_convergence.py
tests/test_critical_smoothing_error.py
```
