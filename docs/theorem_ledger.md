# Theorem Ledger

Each entry records a precise claim, its proof status, and dependencies.
Numerical observations are **never** labeled as proofs of the universal conjecture.

Status labels: `SOURCE_THEOREM` | `PROVED_LOCALLY` | `FORMALIZED` | `CONJECTURE` | `NUMERICAL_OBSERVATION` | `DISPROVED` | `UNVERIFIED`

---

## T001 — Jordan curve square peg conjecture (Toeplitz)

**Statement.** For every continuous injective map γ: S¹ → ℝ², there exist four distinct parameters t₁, t₂, t₃, t₄ such that γ(t₁), …, γ(t₄) are vertices of a nondegenerate square.

**Assumptions.** γ is a Jordan curve (simple closed curve); square vertices are distinct with positive side length.

**Status.** CONJECTURE

**Source.** Otto Toeplitz, 1911

**Dependencies.** —

**Known failure modes.** Approximation proofs without uniform side-length control; parity arguments without diagonal exclusion.

---

## T002 — Noncollapse compactness lemma (extraction)

**Statement.** If γₙ → γ uniformly and each γₙ has an inscribed square with side length ≥ ε > 0, then some subsequence of squares converges to a nondegenerate inscribed square on γ.

**Assumptions.** Uniform convergence of Jordan curves; fixed ε > 0 lower bound on side length.

**Status.** PROVED_LOCALLY

**Source / proof file.** Standard compactness; to be formalized in `formal/SquarePeg/`

**Dependencies.** T001 (motivation only)

**Known failure modes.** Without ε, limiting vertices may coincide (diagonal escape).

---

## T003 — Greene–Lobb derivative property

**Statement.** For smooth Jordan curves γ in an open dense subclass, the spectral invariant ℓ(γ, θ) is differentiable at almost every θ, and ℓ′(γ, θ) = R(P)² for a spectral inscribed θ-rectangle P, where R(P) is half the diagonal length.

**Assumptions.** Smooth Jordan curve; spectral invariant from Jordan Floer homology as in Greene–Lobb.

**Status.** SOURCE_THEOREM

**Source.** Greene & Lobb, arXiv:2604.17116 (April 2026), Theorem 5.1

**Dependencies.** Jordan Floer homology (Greene–Lobb arXiv:2404.05179)

**Known failure modes.** Does not by itself force θ = π/2; derivative property is proved for smooth curves, then passed to limits.

---

## T004 — Midpoint extraction lemma (Proposition A)

**Statement.** If a C⁰-limit ℓ of spectral invariants along smooth approximations satisfies positive midpoint spectral density m(γ, ℓ) > 0 at θ = π/2, then γ contains a nondegenerate inscribed square.

**Assumptions.** Uniform convergence ℓₙ → ℓ; absolute continuity; derivative-to-radius property on approximants; m(γ, ℓ) = limsup_{h↓0} (ℓ(π/2+h) − ℓ(π/2−h)) / (2h) > 0.

**Status.** PROVED_LOCALLY

**Source / proof file.** `docs/spectral_midpoint_route.md` (planned); mechanism in Greene–Lobb arXiv:2604.17116, proof of Theorem A / Corollary 2.2

**Dependencies.** T002, T003

**Known failure modes.** Requires a limit ℓ with positive midpoint slope; different approximation sequences may yield different limits.

---

## T005 — Midpoint nonflatness conjecture

**Statement.** Every Jordan curve γ admits at least one smooth approximation sequence whose limiting spectral invariant has m(γ, ℓ) > 0 at θ = π/2.

**Assumptions.** Jordan curve; spectral invariants from Jordan Floer / Greene–Lobb framework.

**Status.** CONJECTURE

**Source.** Research program reduction (June 2026)

**Dependencies.** T004 (implies T001 if true)

**Known failure modes.** ℓ may be infinitesimally flat at π/2 while satisfying global monotonicity, Lipschitz, and triangle-inequality axioms (to be tested in Milestone 3).

---

## T006 — Asano–Ike square-angle diagonal vanishing (target)

**Statement.** For a Jordan curve C with limiting sheaf F_C, let a = a(π/2, C) be the square-angle critical value. Then microlocal cohomology supported on ρ⁻¹(Δ_C) vanishes for μhom(F_C, T⁻ᵃ R_{π/2} F_C), implying a genuine inscribed square when the continuous Legendrian-lift hypotheses hold.

**Assumptions.** Asano–Ike Tamarkin-category framework; square angle θ = π/2; Z₄ symmetry mechanism (proposed).

**Status.** CONJECTURE

**Source.** Asano & Ike arXiv:2412.21057 v3 (Jan. 2026); square-angle specialization in research plan

**Dependencies.** T005 (alternative bridge to T001)

**Known failure modes.** Z₄ action may not commute with filtration; lift hypothesis fails on measure-zero nonrectifiable curves.

---

## T007 — All polygons inscribe a square

**Statement.** Every simple polygon in the plane has at least one nondegenerate inscribed square.

**Assumptions.** Piecewise-linear Jordan curve (polygon).

**Status.** SOURCE_THEOREM

**Source.** Pak (2008); see also Matschke survey

**Dependencies.** —

**Known failure modes.** Polygonal counterexamples do not exist; collapse under refinement is the relevant limit phenomenon, not absence on finite polygons.

---

## T008 — Exact edge-quadruple linear reduction (polygons)

**Statement.** For a fixed cyclic quadruple of polygon edges eᵢ(uᵢ) = aᵢ + uᵢ dᵢ, inscribed squares with vertices on those edges satisfy six linear equations in (u₁, u₂, u₃, u₄, vₓ, vᵧ) for each choice of J = ±90° rotation.

**Assumptions.** Simple polygon; vertices in edge interiors or endpoints with uᵢ ∈ [0, 1].

**Status.** PROVED_LOCALLY

**Source / proof file.** `src/squarepeg/exact_squares/solver.py`; `artifacts/directive_001_report.md`

**Dependencies.** T007 (existence); this is a computational characterization, not an independent existence proof.

**Known failure modes.** Rank-deficient systems yield positive-dimensional families; repeated-edge quadruples require parameter-order checks.

---

## T009 — Polygon solver enumeration completeness (finite)

**Statement.** Every nondegenerate square inscribed in a simple polygon is represented by at least one cyclic edge quadruple examined by the solver (for some choice of \(J=\pm 90^\circ\)), modulo deduplication of geometrically identical squares.

**Assumptions.** Simple polygon; exact rational isolated certification; rank \(\leq 4\) families may be marked unsupported.

**Status.** PROVED_LOCALLY

**Source / proof file.** `docs/polygon_solver_completeness.md`

**Dependencies.** T008

**Known failure modes.** Rank \(\leq 4\) feasibility not fully certified; float inputs unresolved.

---

## T010 — Solver soundness (isolated certificates)

**Statement.** Every emitted `exact` certificate passes independent geometric and equation validation.

**Assumptions.** `validator.py` independent of production equation module path; rational arithmetic exact.

**Status.** PROVED_LOCALLY (computational proposition, tested on corpus)

**Source / proof file.** `src/squarepeg/exact_squares/validator.py`; `tests/test_independent_validation.py`

**Dependencies.** T008

**Known failure modes.** Validator does not prove universal polygon correctness—only per-certificate checks.

---

## T011 — Affine 1D family exact representation

**Statement.** Rank-5 edge-quadruple systems are certified by `AffineSquareFamily1D` with exact base point, direction, feasible parameter intervals, and excluded degenerate parameters—without sampling as the mathematical result.

**Assumptions.** Six-equation linear model; feasibility intersection exact over \(\mathbb{Q}\).

**Status.** PROVED_LOCALLY

**Source / proof file.** `src/squarepeg/exact_squares/families.py`

**Dependencies.** T008

**Known failure modes.** Rank \(\leq 4\) returns `UnsupportedHigherDimensionalFamily`.

---

## T012 — Midpoint extraction lemma (abstract)

**Statement.** Uniform convergence of normalized spectral invariants along smooth approximants, combined with the derivative property on approximants and a uniform positive symmetric slope near x = 1/2, implies a nondegenerate inscribed square on the limit curve.

**Assumptions.** See `docs/midpoint_extraction_lemma.md`; no pointwise convergence of derivatives assumed.

**Status.** PROVED_WITH_STRENGTHENED_HYPOTHESIS

**Source / proof file.** `docs/midpoint_extraction_lemma.md`; audit: `docs/midpoint_extraction_audit.md`

**Dependencies.** T002, T003

**Known failure modes.** Requires uniform slope hypothesis (H-uniform); uniform convergence alone insufficient (diagonal gap).

---

## T013 — Level-F midpoint forcing at κ = 1

**Statement.** Level-F axioms with κ = 1 force g(x) = x and D⁺(g, 1/2) = 1.

**Assumptions.** Normalized functional axioms (endpoints, 1-Lipschitz, monotonicity).

**Status.** DERIVED

**Source / proof file.** `docs/functional_countermodels.md`

**Dependencies.** P6 normalization

**Known failure modes.** —

---

## T014 — Level-F countermodel (Directive 003 claim — RETRACTED)

**Original statement (Directive 003).** Continuum Level-F countermodel at κ ≥ 11/10 with D⁺(g, ½) = 0.

**Status.** **RETRACTED** (Directive 003R audit)

**Replacement — T014W (Model W only).** Nondecreasing PL from N=40 grid at κ=11/10. **Superseded for Model S** by T015.

**Status (T014W).** PROVED_LOCALLY (Model W only; historical)

---

## T015 — Strict smooth Level-F countermodel (Model S)

**Statement.** The normalized Level-F axioms for Model S admit the strict smooth countermodel

\[
g_*(x)=4x^3-6x^2+3x
\]

for every \(\kappa\ge3\), with \(D^+(g_*,\tfrac12)=0\). Subadditivity proved algebraically: \(H(x,y)=12xy(1-x-y)\ge0\).

**Assumptions.** Scalar functional axioms only; \(\kappa=\pi R^2/A\); not claimed realizable by Jordan Floer.

**Status.** PROVED_LOCALLY

**Source / proof file.** `docs/cubic_countermodel_proof.md`; `cubic_countermodel.py`; `cubic_independent_verify.py`

**Dependencies.** —

**Known failure modes.** Does not satisfy spectrality, Floer grading, or derivative=radius² for genuine rectangles. Applies only for \(\kappa\ge3\), not \(1<\kappa<3\).

**Supersedes:** Directive 003R Outcome B for Model S (κ≥3).

---

## T016 — Residual square-angle vanishing

**Statement.** For \(C\in\mathcal{R}\) (measure-zero residual class), microlocal Hom on \(\rho^{-1}(\Delta_C)\) vanishes at square angle with translation \(-a(\pi/2,C)\). See `docs/residual_square_angle_vanishing.md`.

**Status.** CONJECTURAL_TARGET

**Conditional consequence.** Universal square peg if combined with AI-PEG-v3 solved classes.

---

## T017 — Finite p-variation rectangular peg bridge

**Statement.** Jordan \(c\) with finite \(p\)-variation for some \(1\le p<2\) satisfies AI-PEG-v3 Theorem 1.1 and inscribes every \(\theta\)-rectangle.

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** release `t017-verified-release-2026-06-18`

**Release manifest:** `artifacts/t017_verified_release_manifest.json`

**Source / proof file.** `docs/finite_p_variation_bridge.md`, `docs/t018_velocity_matched_cubic.md`, `docs/t017_frozen_statement.md`

**Dependencies.** BG-INTERPOLATION-v2; AI-PEG-v3; T018 (cubic).

**Do not alter frozen proof without a new release tag.**

---

## T018 — Controlled C¹ polygon smoothing

**Statement.** Simple polygonal Jordan \(P\) admits regular \(C^1\) Jordan \(S\) with common parametrization and \(\|S-P\|_{q\text{-var}}<\varepsilon\).

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** (same release)

**Source / proof file.** `docs/t018_velocity_matched_cubic.md`

---

## T019 — Finite-(2)-variation rectangular peg

**Statement.** Every Jordan curve of finite 2-variation inscribes every \(\theta\)-rectangle.

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** release `t019-t021-verified-release-2026-06-18`

**Release manifest:** `artifacts/t019_t021_verified_release_manifest.json`

**Source / proof file.** `docs/finite_2variation_rectangular_peg.md`

---

## T021 — Simple-arc area–variation inequality

**Statement.** \(|\mathcal A_\alpha(s,t)|\le\frac\pi4|\alpha|_{2-var;[s,t]}^2\).

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** (same release)

**Source / proof file.** `docs/simple_arc_area_variation_inequality.md`

---

## T022 — Area-tight rectangular peg criterion

**Statement.** Area-tight polygonal sequence \(\Rightarrow\) Asano–Ike.

**Status.** PROVED_LOCALLY (Directive 010)

**Source / proof file.** `docs/area_tight_rectangular_peg_criterion.md`

---

## T023 — Universal area-tightness

**Statement.** Every Jordan curve admits area-tight PL approximants.

**Status.** CONJECTURAL_FULL_BRIDGE

---

## T024 — Double-spiral area obstruction

**Statement.** \(\Gamma_{\mathrm{ds}}\) has no area-tight inscribed polygon sequence.

**Status.** CONJECTURAL_TARGET (Directive 010 — not proved)

---

## T020 — Critical-modulus rectangular peg

**Statement.** Jordan curve with critical modulus \(\int m(r)^2/r\,dr<\infty\) satisfies AI-PEG-v3 Theorem 1.1.

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED — **FROZEN** release `t020-verified-release-2026-06-18`

**Release manifest:** `artifacts/t020_verified_release_manifest.json`

**Source / proof file.** `docs/critical_modulus_rectangular_peg.md`, `docs/t020_clean_room_audit.md`

**Historical:** Directive 008 Outcome B superseded (F011 closed).

**Do not alter frozen proof without new release tag.**

---

## Directive 005 verdict (historical)

**OUTCOME B — APPROXIMATION OBSTRUCTION.** Unresolved: PL → \(C^1\) with \(q\)-variation convergence. Superseded by T018 / Directive 006 Outcome A.

---

## Historical note — Directive 003R Outcome B

Outcome B (Model W only) remains in the record via T014W. **Superseded for Model S** by T015 as of Directive 004.

---

## M001 — Rank ≤4 polygon-family gap

**Statement.** Classify rank-≤4 edge-quadruple square systems; do not silently discard.

**Status.** UNVERIFIED (maintenance)

**Source / proof file.** `docs/missing_axiom_candidates.md`

**Benchmark scan (Directive 003).** No rank-≤4 unsupported systems in `data/benchmark_polygons.json`.

---

## Warning (Directive 002–003)

T008–T011 concern **finite simple polygons**. T012–T014 concern **abstract spectral functionals**; they do not prove or disprove the Toeplitz conjecture for arbitrary Jordan curves.

