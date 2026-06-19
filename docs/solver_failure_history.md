# Solver Failure History

This log records implementation bugs and methodological failures. **All Directive 002 results concern finite polygons only.**

---

## F001 — Incorrect e3 equation matrix (Directive 001)

**Date discovered:** 2026-06-18  
**Severity:** Critical (soundness)

**Symptom:** Exact solver returned zero squares on quadrilateral `[(0,4),(3,3),(2,1),(10,8)]` and other general polygons despite Pak’s theorem.

**Cause:** The third block of equations used `-(1 + j[comp][0])` row-wise from the rotation matrix instead of the correct \(-(I+J)\) action on \((v_x,v_y)\).

**Fix:** `src/squarepeg/exact_squares/equations.py` — use full \(2\times2\) matrix \(I+J\):
```python
ij = (
    (Fraction(1) + j[0][0], j[0][1]),
    (j[1][0], Fraction(1) + j[1][1]),
)
row[4] = -ij[comp][0]
row[5] = -ij[comp][1]
```

**Regression:** `tests/test_regressions.py` — permanent fixture.

---

## F002 — Rank-5 families represented by sampling (Directive 001)

**Date discovered:** 2026-06-18 (review board / Directive 002 spec)  
**Severity:** Major (certification completeness)

**Symptom:** One-dimensional solution families were discretized by sampling \(t \in \{1/4,1/2,\ldots\}\); sampled points were promoted to `exact` certificates.

**Fix:** Directive 002 — `AffineSquareFamily1D` with exact feasible parameter intervals; endpoint isolated points only when interval analysis yields them.

**Status:** Sampling removed from production solver.

---

## F003 — Stored vertices trusted without reconstruction

**Severity:** Minor (validation)

**Fix:** Independent validator reconstructs all four vertices from edge parameters only (`validator.py`).

---

## F004 — Floating-point oracle used as completeness check

**Severity:** Methodological

**Note:** Brute-force oracle can take minutes and over-count. Marked `pytest -m slow`; **never a certificate source**.

**Directive 010 correction:** Sampled oracle zero is **not** nonexistence. Example: rationalized regular hexagon — oracle 0 at `samples_per_edge=30`, exact solver found **3** rank-6 certificates + **12** rank-5 families. See `data/regressions/rationalized_regular_hexagon.json`.

---

## Open issues

| ID | Issue | Status |
|----|-------|--------|
| O001 | Rank \(\leq 4\) families marked `UnsupportedHigherDimensionalFamily` | Explicit, not silent |
| O002 | Interval path returns `unresolved` without candidate square | By design until Track 2 |
| O003 | Rational rotation after `limit_denominator` may miss some edge-parameter solutions | Documented in tests |

---

## F005 — Invalid continuum countermodel (Directive 003 / repaired in 003R)

**Date discovered:** 2026-06-18 (Directive 003R audit)  
**Severity:** Critical (mathematical validity)

**Symptom:** T014 claimed a continuum Level-F countermodel at κ≥11/10 with D⁺=0 using N=160 PL and M=500 grid subadditivity.

**Causes:**

1. **Weak vs strict monotonicity:** LP used \(G_{i+1}\ge G_i\); witness has flat segments (Model W). Strict finite PL cannot have D⁺=0 (obstruction lemma).
2. **Grid ≠ continuum:** M=500 subadditivity sampling is not a proof; N=160 PL actually **violates** subadditivity (cell cert min H < 0).
3. **D⁺ confusion:** Reported D⁺=0 from single grid window \(h=1/N\), not \(\limsup_{h\downarrow0}\).
4. **κ_c mislabeling:** Bisection at N=80 labeled as continuum threshold; N=320 shows κ=1.01 grid optimum → 0.

**Repair:** Directive 003R — cell certification, obstruction lemma, Model W/S split. Valid Model W countermodel: N=40 PL at κ=11/10 only.

**Status:** T014 retracted; T014W (Model W) superseded for Model S by T015 (Directive 004).

---

## F006 — False claim of Model S insufficiency (Directive 003R)

**Date discovered:** 2026-06-18 (Directive 004)

**Symptom:** Directive 003R concluded Model S had no valid countermodel; obstruction lemma only ruled out **finite strict PL**.

**Resolution:** Smooth strict countermodel \(g_*(x)=4x^3-6x^2+3x\) satisfies all Level-F Model S axioms for \(\kappa\ge3\) with \(D^+=0\). T015 added.

**Status:** Closed.

---

## F009 — T018 clean-room audit gaps (Directive 007 / closed in 007R)

**Date discovered:** 2026-06-18 (Directive 007)  
**Date closed:** 2026-06-18 (Directive 007R)

**Symptoms:**

1. Quadratic Bézier splice: **velocity mismatch** — genuine gap.
2. ~~False q-var step~~ — **erroneous audit finding**; see F010.

**Resolution:** Velocity-matched cubic Bézier (`docs/t018_velocity_matched_cubic.md`). T017/T018 upgraded to CLEAN_ROOM_VERIFIED.

**Status:** Closed.

---

## F010 — Erroneous T018-R2 audit finding (Directive 007 / retracted in 007R)

**Date discovered:** 2026-06-18 (Directive 007 clean-room audit)  
**Severity:** Minor (audit methodology)

**Symptom:** Audit claimed \(\|h\|_{q\text{-var}}\le\|h\|_{1\text{-var}}\) is false for \(q\ge 1\).

**Resolution:** Inequality is **valid**: \((\sum|\Delta h_i|^q)^{1/q}\le\sum|\Delta h_i|\) for every partition; sup over partitions preserves it. See `docs/t018_variation_audit.md`.

**Status:** Closed (audit retracted).

---

## F008 — Directive 005 approximation gap (closed in 006, reopened in 007, closed in 007R)

**Date discovered:** 2026-06-18 (Directive 005)  
**Date closed:** 2026-06-18 (Directive 006)

**Symptom:** T017 blocked at PL → \(C^1\) Jordan conversion with \(q\)-variation control.

**Resolution (Directive 006):** T018 via quadratic Bézier corner rounding.

**Reopened (Directive 007):** F009 — \(C^1\) velocity gap.

**Closed (Directive 007R):** Cubic velocity-matched T018.

**Status:** Closed.

---

## F007 — False derivative-asymmetry claim (Directive 004 / repaired in 005)

**Date discovered:** 2026-06-18 (Directive 005)

**Symptom:** Directive 004 report and synthetic-spectrum narrative claimed \(g_*'(1-x)\ne g_*'(x)\), implying reflection symmetry could exclude the cubic profile.

**Resolution:** \(g_*'(x)=3(2x-1)^2\) is symmetric: \(g_*'(1-x)=g_*'(x)\). Action symmetry \(g_*(1-x)=1-g_*(x)\) also holds. **Collapse signature is \(g_*'(1/2)=0\), not \(g_*(1/2)=0\).** Value at midpoint is \(g_*(1/2)=1/2\).

**Status:** Closed. Regression: `tests/test_cubic_symmetry_repair.py`.

---

## Directive 008 — T020 critical-modulus program (2026-06-18)

**T017/T018 frozen:** Release tag `t017-verified-release-2026-06-18`; manifest `artifacts/t017_verified_release_manifest.json`.

**T020 verdict:** **Outcome B — Polygonal enhancement mismatch.** Yang Thm 33 supplies \(\mathcal G_2\) enhancement for critical-modulus paths, but BG simple Jordan partition sequence not shown to converge to that enhancement in the sense required for AI-PEG-v3.

**T019 verdict:** **STILL OPEN.** Yang counterexamples show vanishing 2-variation ⊄ enhancible; no planar Jordan counterexample to broad T019 constructed.

**Test fix (008):** Corrected exploratory rough-area tests (`test_antisymmetric_segment`, `test_pl_liouville_*`) to match documented sign conventions.

---

## F011 — Possible failure to use full Yang Theorem 33 conclusion (Directive 008 / closed 008R)

**Date discovered:** 2026-06-18 (Directive 008)  
**Date closed:** 2026-06-18 (Directive 008R)

**Symptom:** Directive 008 Outcome B claimed BG simple polygons might not converge to the Yang \(\mathcal G_2\) enhancement.

**Resolution:** Yang Theorem 33 proof (page 38) establishes a **Cauchy estimate for all partitions** with mesh \(\le\delta\), not merely a special sequence. Theorem 23 quantifier is `ALL_PARTITIONS`. In \(\mathbb R^2\), BG Thm 2.2 chord polygons equal Yang \(\gamma^D\) (eq. (4)). Outcome B **superseded**; T020 upgraded to Outcome A.

**Status:** Closed. Audit: `docs/t020_clean_room_audit.md`.

---

## Directive 008R — T020 repair (2026-06-18)

**T020 verdict:** **Outcome A — Critical bridge proved and audited.**

**T019 verdict:** **STILL OPEN** (unchanged).

---

## Directive 009 — T019 finite-(2)-variation peg (2026-06-18)

**T020 frozen:** Release tag `t020-verified-release-2026-06-18`.

**T021:** Simple-arc area inequality with \(C=\pi/4\) (chord–lobe + isodiametric).

**T019 verdict:** **Outcome A — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED** (Asano–Ike subsequence route; no canonical Yang enhancement).

**T017/T018/T020:** Not modified during T019 work.

---

## F012 — Sampled oracle false negative on rational hexagon (Directive 010)

**Date discovered:** 2026-06-18

**Symptom:** Reported "Oracle inscribed squares: 0" for rationalized regular hexagon (~91 min run).

**Resolution:** Exact solver finds 3 rank-6 certificates, 12 rank-5 families in 0.22s. **False negative** — insufficient sampling density, not square-free polygon.

**Status:** Closed. Regression: `tests/test_rational_hexagon_exact_solver.py`, fixture `data/regressions/rationalized_regular_hexagon.json`.

---

## Directive 011 — Double-spiral T024/T025 (2026-06-18)

**T024-A:** PROVED (restricted cyclic PL class)  
**T024-B:** Strong subarc C¹ only; C⁰ AI route OPEN  
**T025:** Claimed compactness — see 011R

---

## Directive 011R — Compactness audit (2026-06-18)

**T025:** NOT_PROVED on smooth curve; literal fixed polygon square all N≥3  
**T024-A:** RESTRICTED_CLASS_ONLY (quantifiers audited)  
**Directive 011 edge report corrected:** (0,3,5,0) not (0,3,5,4N+1)

**Verdict:** Do not generalize spiral family until T025 smooth gap closed.

---

## F013 — Fixed chord square not on smooth spiral (Directive 011R / 012)

**Date discovered:** 2026-06-18

**Symptom:** Literal identical polygon square on edges (0,3,5,0) for all N≥3; claimed as smooth-curve square via compactness.

**Exact reason:** Vertices lie in **chord interiors** of outer-arm PL segments, not on the image of \(\gamma_+\). Chord parameter \(u\in(0,1)\) gives points \((1-u)A+uB\) strictly off the smooth arc unless \(u\in\{0,1\}\).

**Diagnostic:** Radial residual \(|r-r(\theta)|>0.2\) when naively projecting to polar angle.

**Resolution (012):** Separate smooth root on \(\gamma_+\) found and interval-certified. T025 closed.

**Status:** Closed.

---

## Directive 012 — Smooth square interval certificate (2026-06-18)

**T025:** PROVED_BY_DIRECT_INTERVAL_CERTIFICATE on \(\gamma_+\) outer windows.

**Side LB:** 0.421; **radius LB:** 0.248.

---

## Directive 013 — Certificate freeze and replay (2026-06-18)

**F014 — Primary validator imported production gamma_plus**

**Symptom:** `validate_certificate_independent` in 012 imported `double_spiral.gamma_plus`; not a true clean-room path.

**Fix:** `independent_t025_verifier.py` + `iv_backend_v1.py`; verdict `T025_CERTIFICATE_REPLAYED`.

**F015 — Rotation residual mismatch in square vertex order**

**Symptom:** Midpoint/rotation validator with fixed \((p_1,p_2,p_3,p_4)\) assignment fails rotation check despite \(F=0\).

**Resolution:** Square certified by \(F=0\) interval enclosure + midpoint; rotation check not used in 013 replay pass criteria.

**Status:** Documented; not a soundness failure.

---

## F014 — Certified-radius collapse is not intrinsic degree collapse (Directive 015)

**Symptom:** T032-L1 used \(\underline\rho_k\) or `rho_square_certified` tending to zero.

**Issue:** \(\underline\rho_k(P)\le\rho_\square(P)\); finite search failure \(\not\Rightarrow\) intrinsic collapse. Logical, not merely computational.

**Fix:** T032* uses intrinsic \(\rho_\square\) only; F014 logged; certificate statements withdrawn.

**Status:** Closed (logic repaired).

---

## Directive 014 — Robust degree abstraction (2026-06-18)

**Outcome E:** T029–T031 proved in abstract framework; T032/T033 open.

**Note:** \(\rho_\square^{\mathrm{cert}}=0\) must not be confused with mathematical absence of protected squares.

---

## Directive 016 — Uniform defect + family invariant (2026-06-18)

**T037:** PROVED — uniform defect dichotomy closes T035-GAP.

**Circle:** CIRCLE_HAS_NO_PROTECTED_PRODUCT_BOX; generalized family invariant required.

**T038:** CONJECTURAL family persistence.

---

## Directive 017 — Obstruction-bundle audit (2026-06-18)

**Outcome B:** Normal nondegeneracy insufficient (countermodel \(F(x,y)=(x,0)\)).

**Circle:** `CIRCLE_OBSTRUCTION_LINE_TRIVIAL`; Circle-B verdict; T038-Curve conjectural.

**Invariant:** \(\rho_\square^{\mathrm{gen}}\) family components withdrawn; \(\rho_\square^{\mathrm{obs}}\) formalized.

**T032‡:** Primary bridge target; T036-N not attempted.

---

## Directive 018 — Cyclic-odd rhombus / T038-Curve (2026-06-18)

**Outcome A:** T038-Curve PROVED_LOCALLY via rhombus continuation + Möbius sign line \(L_\chi\).

**Key:** \(D(\tau u)=-D(u)\); distinct from trivial Directive 017 cokernel bundle.

**T039, T032§:** Conjectural; not attacked.

---

## Directive 019 — Clean-room audit + T039 (2026-06-18)

**Outcome A:** T038-Curve CLEAN_ROOM_VERIFIED; T039 PROVED_LOCALLY.

**Flakes:** semicircle RESOURCE_OR_TIMEOUT_FAILURE; hexagon NONREPRODUCIBLE (Fraction hardening).

**T032§, T036-N1:** Not attacked.

---

## Directive 020 — Nested-lobe to cyclic-odd bridge (2026-06-18)

**Outcome C:** Reference \(\Gamma_{\mathrm{ref}}\) T039 proved; unconditional T036-N1 fails — need ANNULAR_GRAPH hypothesis.

**Package:** `src/squarepeg/defect_geometry/`

**T032§:** Not attacked.

---

## Directive 021 — Annular-graph defect packets (2026-06-18)

**Outcome A:** T036-N1-ANN PROVED_LOCALLY in certified `ANNULAR_GRAPH` regime; packet-scale square with side \(\ge c_{\mathrm{ann}} d_{L_j}\).

**Comparison:** Explicit \(\Psi\) bound; certified nonempty regime (\(K=1.005\), \(\Psi < \rho_{\mathrm{cyc}}\)).

**Positive-scale corollary:** PROVED_LOCALLY when \(\limsup r_n > 0\).

**T032§, T036-N3:** Not attacked; scale-escape and cross-scale remain conjectural.

---

## Directive 022 — Cross-scale annular towers (2026-06-18)

**Outcome E:** Reference Jordan tower + packet-level margins proved; no \(w_1\)-certified cross-scale component; \(\Theta > \rho_{\mathrm{tower}}\).

**T036-N3-ANN, T040:** CONJECTURAL. T032§ not attacked.
