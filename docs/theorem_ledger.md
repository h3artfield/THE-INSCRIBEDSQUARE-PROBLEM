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

**Status.** **FALSE** for canonical double spiral (T024-A); conjecture open in general

---

## T024 — Double-spiral area obstruction

**Statement.** No area-tight **cyclic inscribed polygonal interpolation** sequence for \(\Gamma_{\mathrm{ds}}\).

**Status.** **T024-A RESTRICTED_CLASS_ONLY** (Directive 011R quantifier audit)

**T024-B:** Strong subarc \(C^1\) primitive obstruction **proved**; **\(C^0\) Asano–Ike route OPEN**

**Source / proof file.** `docs/t024_quantifier_audit.md`, `docs/t024_strong_topology_obstruction.md`, `docs/double_spiral_no_area_tightness.md`

---

## T025 — Canonical double-spiral square

**Statement.** The canonical double spiral contains a nondegenerate inscribed square.

**Status.** **PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE** (Directive 013 freeze)

**Historical:** 011 claimed compactness; 011R **NOT_PROVED** (chord vertices); 012 interval cert on \(\gamma_+\); 013 independent replay + degree + C⁰ robustness.

**Source / proof file.** `docs/smooth_square_interval_certificate.md`, `docs/t025_certificate_replay.md`, `artifacts/t025_verified_internal_manifest.json`

**Tag:** `t025-smooth-double-spiral-internal-2026-06-18`

---

## T027 — Robust double-spiral support square

**Statement.** Explicit \(\eta_0>0\) such that any four \(C^0\) perturbations of the canonical support pieces within \(\eta_0\) yield a nondegenerate square in the same parameter boxes.

**Status.** **PROVED_LOCALLY_CLEAN_ROOM_VERIFIED** (Directive 013)

**Source / proof file.** `docs/t027_c0_robust_square_theorem.md`

---

## T028 — Wild-tail stability

**Statement.** Jordan curves matching canonical support pieces within \(\eta_0\) on four windows contain an inscribed square regardless of wild tail behavior.

**Status.** **PROVED_AS_COROLLARY** (via T027)

**Source / proof file.** `docs/t028_wild_tail_corollary.md`

---

## T026 — Area-tight-or-protected-square dichotomy

**Statement.** Every Jordan curve either admits an area-tight simple polygonal approximation sequence, or contains a four-window configuration with **nonzero square-map Brouwer degree**.

**Status.** CONJECTURAL_FULL_BRIDGE (refined Directive 013–014)

**Source.** `docs/area_tight_or_square_dichotomy.md`, `docs/t026_missing_universal_lemma.md`, `docs/degree_collapse_to_area_tightness.md`

**Do not attempt proof in Directive 014.**

---

## T029 — Protected square degree theorem

**Statement.** Protected square box \((\gamma,B)\) \(\Rightarrow\) nondegenerate inscribed square in \(B\).

**Status.** PROVED_LOCALLY (Directive 014)

**Source / proof file.** `docs/protected_square_degree.md`, `src/squarepeg/robust_degree/`

---

## T030 — Robust square openness

**Statement.** \(\rho_\square(\gamma,B)>0\) \(\Rightarrow\) all sufficiently \(C^0\)-close curves have inscribed squares.

**Status.** PROVED_LOCALLY (Directive 014; recovers T027)

**Source / proof file.** `docs/robust_square_radius.md`

---

## T031 — Positive robust-degree limit criterion

**Statement.** \(\limsup_n\rho_\square^{\mathrm{cert}}(P_n,B)>0\) with compatible windows \(\Rightarrow\) limit curve has square.

**Status.** PROVED_LOCALLY (Directive 014)

**Source / proof file.** `docs/robust_degree_limit_criterion.md`

---

## T032* — Intrinsic degree-collapse-to-area-tightness

**Statement.** Intrinsic \(\rho_\square(P_{n_k})\to 0\) on compatible windows \(\Rightarrow\) area-tight subsequence.

**Status.** CONJECTURAL_FULL_BRIDGE (replaces certificate-based T032 — withdrawn F014)

**Source / proof file.** `docs/t032_intrinsic_bridge.md`

---

## T033 — Finite-scale dichotomy

**Status.** FINITE_SCALE_DICHOTOMY_TARGET

---

## T034 — Protected-box semidecidability (rational polygons)

**Statement.** Intrinsic \(\rho>\eta\) \(\Rightarrow\) exhaustive search eventually certifies \(\underline\rho_k>\eta'\) for all \(\eta'<\eta\).

**Status.** PROVED_LOCALLY (Directive 015)

**Source / proof file.** `docs/protected_box_semidecidability.md`

---

## T035 — Area-tight subsequence criterion

**Statement.** Diagonal criterion with \(\delta_j=2^{-j}\) equivalent to area-tightness.

**Status.** PROVED_LOCALLY (Directive 015)

**Source / proof file.** `docs/area_tight_subsequence_selection.md`

---

## T037 — Uniform defect subsequence dichotomy

**Status.** PROVED_LOCALLY (Directive 016)

**Source / proof file.** `docs/uniform_defect_selection.md`

---

## T038 — Protected square family persistence

**Status.** CONJECTURAL (superseded by T038′ — normal index alone insufficient, Directive 017)

**Source / proof file.** `docs/protected_square_families.md`, `docs/obstruction_bundle_persistence_theorem.md`

---

## T038′ — Obstruction-bundle square-family persistence

**Statement.** Compact Morse-Bott family with \(\langle w_d(E),[Z]_2\rangle\ne0\) persists under small \(C^0\) perturbations.

**Status.** CONJECTURAL_TARGET — algebraic framework and countermodel complete; full analytic proof with tubular neighborhood hypotheses not closed (Directive 017–018)

**Source / proof file.** `docs/obstruction_bundle_persistence_theorem.md`

---

## T038-Curve — Cyclic-odd circle-family persistence

**Statement.** Every Jordan curve sufficiently close to the unit circle in \(C^0\) has a nondegenerate inscribed square in the cyclic-invariant neighborhood \(U\).

**Status.** PROVED_LOCALLY (Directive 018)

**Source / proof file.** `docs/t038_curve_circle_proof.md`, `docs/cyclic_odd_persistence_theorem.md`

---

## T039 — Cyclic-odd rhombus continuation (general)

**Statement.** Admissible cyclic-invariant rhombus components with sign-line obstruction persist under small \(C^0\) curve perturbations.

**Status.** CONJECTURAL_GENERALIZATION (Directive 018)

**Source / proof file.** `docs/t039_general_cyclic_odd_theorem.md`

---

## T032§ — Admissible-protected collapse to area-tightness

**Statement.** Admissible-protected component radii \(\to0\) \(\Rightarrow\) area-tight subsequence.

**Status.** CONJECTURAL_FULL_BRIDGE (primary over T032‡ if T038-Curve proved)

**Source / proof file.** `docs/admissible_protected_bridge.md`

---

## ρ_square^adm — Admissible protected invariant

**Definition.** Supremum over isolated Brouwer, Euler obstruction, and cyclic-odd rhombus components.

**Status.** FORMALIZED (Directive 018)

**Source / proof file.** `docs/admissible_protected_invariant.md`

---

## T038-Curve (historical entry — Directive 017)

**Status.** Superseded statement — see cyclic-odd proof above.

**Source / proof file.** `docs/curve_induced_circle_sections.md` (first-order calibration)

---

## T032‡ — Obstruction-protected collapse to area-tightness

**Statement.** Obstruction-protected component radii \(\to0\) \(\Rightarrow\) area-tight subsequence.

**Status.** CONJECTURAL_FULL_BRIDGE (primary bridge, Directive 017)

**Source / proof file.** `docs/obstruction_protected_bridge.md`

---

## T032† — Generalized intrinsic bridge

**Status.** CONJECTURAL_FULL_BRIDGE — **superseded as primary** by T032‡ (uses unproved family persistence)

**Source / proof file.** `docs/generalized_intrinsic_bridge.md`

---

## ρ_square^obs — Obstruction-protected invariant

**Definition.** Supremum of persistence radii over admissible protected components (Brouwer, Euler obstruction, or T038-Curve).

**Status.** FORMALIZED (Directive 017); \(\rho_\square^{\mathrm{gen}}\) withdrawn for family components without obstruction proof.

**Source / proof file.** `docs/obstruction_protected_invariant.md`

---

## T036-N — Nested-lobe controlled bridge

**Status.** CONTROLLED_CLASS_TARGET

**Source / proof file.** `docs/nested_lobe_controlled_bridge.md`

---

## T032 (withdrawn)

Certificate-based collapse statement **invalid** — see F014, `docs/intrinsic_vs_certified_robust_degree.md`.

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

