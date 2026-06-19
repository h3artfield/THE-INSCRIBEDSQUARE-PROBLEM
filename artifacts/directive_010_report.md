# Directive 010 Report — Residual Infinite-(2)-Variation Curves

**Date:** 2026-06-18  
**Status:** Complete  
**Verdict:** **Outcome C** — T022 proved locally; T023 and T024 unresolved

---

## Part I — Rational hexagon regression gate

| Item | Result |
|------|--------|
| Fixture | `data/regressions/rationalized_regular_hexagon.json` |
| Vertices | `limit_denominator(1000)` on unit circle at \(k\pi/3\), \(k=0..5\) |
| Simple / convex | yes / yes |
| Signed area | `808/311` |
| Polygon hash | `0348df87312fb4f1ac26c5402d174ea5b8150aea6ee054992bb1cdb7638cb2fd` |
| Exact solver | **3** rank-6 certificates, **12** rank-5 affine families, **0** unsupported rank-≤4 |
| Runtime | ~0.22 s |
| Oracle (samples_per_edge=30) | 0 candidates — **false negative** |

All certificates pass `validate_geometry`. Regression: `tests/test_rational_hexagon_exact_solver.py`.

**Interpretation:** Sampled oracle zero is not nonexistence. Fixture preserved. No additional multi-hour oracle runs.

---

## Part II — T019/T021 freeze

| Theorem | Status |
|---------|--------|
| T019 | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** |
| T021 | PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** |

**Release tag:** `t019-t021-verified-release-2026-06-18`  
**Manifest:** `artifacts/t019_t021_verified_release_manifest.json`  
**Manuscript:** `manuscript/finite_2variation_rectangular_peg.pdf`  
**Review packet:** `review/T019_T021_*` (draft queries — do not send without authorization)

**Novelty audit:** T019 — APPARENTLY NEW SYNTHESIS; T021 — APPARENTLY NEW LEMMA (`docs/t019_t021_novelty_audit.md`).

Frozen proofs were not modified during residual-curve work.

---

## Part III — Area-tightness framework

| Theorem | Status |
|---------|--------|
| T022 | PROVED_LOCALLY — area-tight PL sequence ⇒ Asano–Ike |
| T023 | CONJECTURAL_FULL_BRIDGE — universal area-tightness |
| T024 | CONJECTURAL_TARGET — double-spiral obstruction |

**Docs:** `docs/area_tight_approximation.md`, `docs/area_tight_rectangular_peg_criterion.md`, `docs/t022_clean_room_audit.md`

Area-tightness is weaker than canonical rough enhancement; only one good sequence is required.

**T019 recovery:** finite 2-variation ⇒ T021 bound ⇒ BG polygon sequence area-tight ⇒ T022 ⇒ Asano–Ike.

**T020 recovery:** Yang partition area convergence ⇒ area-tight (shorter route documented; frozen T020 unchanged).

---

## Part IV — Double spiral \(\Gamma_{\mathrm{ds}}\)

| Property | Status |
|----------|--------|
| Jordan | proved (`docs/double_spiral_jordan_proof.md`) |
| Measure zero | yes |
| Infinite length | yes (\(\int r\,d\theta\) diverges) |
| Infinite 2-variation | yes (half-turn partition, \(\sum 1/k\) divergence) |
| Variation index | \(p>2\) finite; \(p\le2\) infinite |
| One-arm action | diverges (\(\sim\log T\)) |
| Enclosed area | finite (arm-width cancellation) |

**Code:** `src/squarepeg/residual_curves/` — `double_spiral.py`, `annular_winding.py`, `area_tightness.py`, `truncated_spirals.py`

**T024:** Not proved. Annular winding certificates give exploratory \(\log N\) area lower bounds for natural inscribed polygons; failure of one sequence ≠ failure of all sequences.

**Missing for T024:** topological lower bound that every sufficiently accurate simple inscribed PL sequence must preserve winding in fixed annuli with uniform signed-area contribution.

---

## Part V — Truncated spiral exact square experiments

Rational PL truncations (`truncated_spirals.rational_truncated_spiral`):

| Turns | Vertices | Isolated squares | norm side / diam (max) |
|-------|----------|------------------|------------------------|
| 1 | 7 | 5 | 0.0009 |
| 2 | 11 | 9 | 0.0009 |
| 3 | 15 | 71 | **0.507** |
| 4 | 19 | 217 | **0.507** |
| 5 | 23 | 523 | **0.507** |
| 6 | 27 | 977 | **0.507** |

Macroscopic squares (side \(\approx\) half diameter) persist through turn 6; micro squares also appear on inner turns. No finite truncation proves anything about the limiting curve.

---

## Part VI — Outcome selection

**Outcome C — Conditional criterion proved, hard curve unresolved**

- T022: proved locally (clean-room audit complete).
- T023: open (universal area-tightness).
- T024: open (exact winding estimate for obstruction).
- T019/T021: frozen, no external acceptance claimed.
- Full square-peg / rectangular-peg conjecture: **not** claimed.

---

## Part VII — Tests and tooling

Fast suite: **175 passed**, 2 deselected (`-m "not slow"`), ~8.6 s.

New tests: rational hexagon exact solver, double-spiral separation/variation/area, annular winding, area-tightness criterion.

**Bug fixed:** `area_tightness.max_relative_area_on_grid` now passes subarcs to `relative_area_increment`.

---

## Oracle language

Historical F012 documents prior misleading wording. Current reports use: *"The sampled floating-point oracle found no candidate at the selected sampling density. This is not a nonexistence result."*

---

## Files created (Directive 010)

```
data/regressions/rationalized_regular_hexagon.json
artifacts/t019_t021_verified_release_manifest.json
artifacts/directive_010_report.md
docs/area_tight_approximation.md
docs/area_tight_rectangular_peg_criterion.md
docs/double_spiral_*.md (5 files)
docs/residual_class_after_t019.md
docs/t022_clean_room_audit.md
docs/t019_t021_novelty_audit.md
manuscript/finite_2variation_rectangular_peg.{tex,pdf}
review/T019_T021_* (4 files)
src/squarepeg/residual_curves/*.py (4 files)
tests/test_rational_hexagon_exact_solver.py
tests/test_double_spiral_*.py (3 files)
tests/test_annular_winding_certificate.py
tests/test_area_tightness_criterion.py
```
