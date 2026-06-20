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

**Statement.** Every degree-one parametrized Jordan curve with \(\|\gamma-\gamma_0\|_\infty<\eta\) has a nondegenerate inscribed square in cyclic-invariant \(U\).

**Status.** PROVED_LOCALLY, **CLEAN_ROOM_VERIFIED** (Directive 019)

**Source / proof file.** `docs/t038_curve_clean_room_audit.md`, `docs/t038_curve_circle_proof.md`

---

## T039 — Cyclic-odd rhombus continuation (general)

**Statement.** Cyclic-odd protected rhombus components persist under small parametrized \(C^0\) perturbations.

**Status.** PROVED_LOCALLY (Directive 019)

**Source / proof file.** `docs/t039_cyclic_odd_persistence.md`

---

## T032§ — Admissible-protected collapse to area-tightness

**Statement.** Admissible-protected component radii \(\to0\) \(\Rightarrow\) area-tight subsequence.

**Status.** CONJECTURAL_FULL_BRIDGE (not attacked Directive 019)

**Source / proof file.** `docs/admissible_protected_bridge.md`

---

## T036-N1 — Nested-lobe cyclic-rhombus lemma

**Status.** CONDITIONAL_PROVED (Directive 020); strengthened by T036-N1-ANN (Directive 021)

**Source / proof file.** `docs/t036_n1_proof.md`, `docs/packet_reference_comparison.md`

---

## T036-N1-ANN — Annular-graph nested-packet square theorem

**Statement.** In certified `ANNULAR_GRAPH` regime, \(\mathcal D_{\mathrm{nest}}^{\mathrm{ann}}\) packets support cyclic-odd protected rhombus; T039 gives square with \(\operatorname{side}(Q) \ge c_{\mathrm{ann}} d_{L_j}\).

**Status.** PROVED_LOCALLY (Directive 021)

**Source / proof file.** `docs/t036_n1_annular_proof.md`, `docs/annular_packet_comparison_bound.md`

**Depth.** Two controlled layers suffice (\(m_0=2\)).

---

## T036-N2 — Scale-escape alternative

**Status.** CONJECTURAL_SELECTION_TARGET

**Source / proof file.** `docs/scale_escape_alternative.md`

---

## T036-N3 — Cross-scale cyclic component

**Status.** CONJECTURAL_CROSS_SCALE_TARGET (Directive 022 Outcome E — no fixed-scale certificate)

**Source / proof file.** `docs/cross_scale_cyclic_component.md`, `docs/t036_n3_annular_proof.md`

---

## T036-N3-ANN — Coherent annular-tower square theorem

**Status.** CONJECTURAL_TARGET

**Source / proof file.** `docs/t036_n3_annular_proof.md`

---

## T040 — Annular packet tower selection

**Status.** CONJECTURAL_SELECTION_TARGET

**Source / proof file.** `docs/annular_packet_tower_selection.md`

---

## T041 — Shrinking-support obstruction

**Statement.** Square vertices in diameter-\(r\) set have side \(\le r\); shrinking packet support cannot yield macroscopic limit square.

**Status.** PROVED_LOCALLY (Directive 023)

**Source / proof file.** `docs/shrinking_support_obstruction.md`

---

## T042 — Local packet surgery lemma

**Hypotheses:** `CHORD_SAFE_ISOLATED_PACKET` — isolated disk; straight chord in \(D\) avoiding retained curve.

**Statement.** Replacement area \(A_{\sigma}(I)=0\); Jordan preserved; \(\|S_I(P)-P\|_\infty \le \operatorname{diam}D\). Area **change** \(|A_{S_I(P)}(J)-A_P(J)|\) not bounded by \(O(r^2)\) without winding bound.

**Status.** PROVED_LOCALLY (chord-safe case)

**Source / proof file.** `docs/isolated_packet_surgery.md`

---

## T043 — Surgery-to-area-tightness (superseded)

**Status.** SUPERSEDED by T043R (Directive 024)

---

## T043R — Signature-controlled surgery-to-area-tightness

**Hypotheses:** `SIGNATURE_CARLESON` (Directive 025): uniform convergence, Jordan, \(r_n^{\max}\to0\), \(\beta_n,\sigma_n,\chi_n\to0\).

**Statement.** Surgered \(Q_n\to\gamma\) uniformly and area-tight; T022 applies.

**Status.** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 025–026)

**Source / proof file.** `docs/signature_controlled_surgery.md`, `t043r_proof.py`

---

## T046 — Ordered annular forest signature theorem

**Status.** PROVED_LOCALLY (Directive 026)

**Source / proof file.** `docs/t046_annular_signature_theorem.md`

---

## T044R — Controlled annular surgery dichotomy

**Status.** PROVED_LOCALLY (Directive 026)

**Source / proof file.** `docs/t044r_controlled_annular_bridge.md`

---

## T045 — Defect-forest extraction

**Status.** CONJECTURAL_FULL_EXTRACTION

**Source / proof file.** `docs/defect_forest_extraction.md`, `docs/universal_defect_extraction.md`

---

## T045R — Universal protected-or-surgery extraction

**Status.** CONJECTURAL_FULL_EXTRACTION (Directive 027; clean-forest path PROVED_LOCALLY)

**Source / proof file.** `docs/universal_defect_extraction.md`

---

## T047 — Finite defect packet trichotomy

**Status.** CONJECTURAL_STRUCTURAL_TARGET

**Source / proof file.** `docs/packet_shape_trichotomy.md`

---

## T048 — Annular subpacket extraction

**Status.** CONJECTURAL_GEOMETRIC_TARGET

---

## T049 — Interleaving cyclic component

**Status.** CONJECTURAL_INTERLEAVING_TARGET; reference **INTERLEAVING_REFERENCE_UNPROTECTED**

---

## T050 — Finite intrusion saturation theorem

**Statement.** Every dirty polygonal lobe with finite intrusion tree satisfies exactly one: two-gate clean saturation; positive geometric scale; ≥4 separated outer gates; or explicit non-Jordan hull obstruction.

**Status.** CONJECTURAL_STRUCTURAL_TARGET (finite-tree case PROVED_LOCALLY for small trees, Directive 028)

**Source / proof file.** `docs/finite_intrusion_saturation.md`

---

## T051 — Local cluster surgery

**Statement.** Two-gate clean saturated cluster admits Jordan-preserving crosscut surgery with \(O(\operatorname{diam}H(C))\) error, compatible with T043R.

**Status.** PROVED_LOCALLY (Directive 028)

**Source / proof file.** `docs/cluster_crosscut_surgery.md`

---

## T052 — Cluster surgery-to-area-tightness

**Statement.** Ordered two-gate cluster forest with `CLUSTER_SIGNATURE_CARLESON` yields area-tight approximation (via T043R).

**Status.** PROVED_LOCALLY for ordered forests with small diameters (Directive 028)

**Source / proof file.** `docs/cluster_signature_carleson.md`

---

## T053 — Finite-intrusion extraction theorem

**Statement.** If dominant dirty lobes have finite intrusion trees saturating to two-gate clusters, extraction is covered by protected-or-surgery framework.

**Status.** CONJECTURAL_TARGET (Directive 028)

**Source / proof file.** `docs/cluster_signature_carleson.md`

---

## T054 — Multi-gate cluster classification

**Statement.** ≥4-gate positive-defect cluster contains two-gate subcluster, admissible protected square, or multicenter residual — not auto-protected by interleaving.

**Status.** CONJECTURAL_MULTIGATE_TARGET (Directive 028)

**Source / proof file.** `docs/multigate_cluster_classification.md`

---

## T055 — Saturated gate graph outerplanarity

**Statement.** Finite saturated cluster with Jordan-disk hull and noncrossing chord embedding has outerplanar intrusion gate graph.

**Status.** PROVED_LOCALLY (Directive 029)

**Source / proof file.** `docs/saturated_gate_graph.md`

---

## T056 — Multi-gate ear lemma

**Statement.** Outerplanar gate graph contains a graph two-gate ear; geometric ear when hull-adjacent.

**Status.** PROVED_LOCALLY (graph level); geometric mapping partial (Directive 029)

**Source / proof file.** `docs/multigate_ear_lemma.md`

---

## T057 — Bounded-gate finite saturation theorem

**Statement.** M_GATE_BOUNDED finite saturated cluster decomposes into two-gate forest or irreducible outerplanar type.

**Status.** PROVED_LOCALLY without geometric ear gap (Directive 029)

**Source / proof file.** `docs/bounded_gate_saturation.md`

---

## T050R — Finite saturation classification

**Statement.** Five-branch classification replacing overstrong T050.

**Status.** CONJECTURAL_STRUCTURAL_TARGET (Directive 029)

**Source / proof file.** `docs/finite_saturation_classification.md`

---

## T053B — Bounded-gate finite-intrusion extraction

**Statement.** Finite intrusion + Jordan hull + M gates + ear hypotheses => T052 => T043R => T022.

**Status.** PROVED_LOCALLY (Directive 030)

**Source / proof file.** `docs/t053b_bounded_gate_extraction.md`

---

## T058 — Hull-adjacent geometric ear theorem

**Statement.** Outerplanar saturated cluster with ≥4 gates contains hull-adjacent geometric subcluster eligible for T051.

**Status.** PROVED_LOCALLY (Directive 030)

**Source / proof file.** `docs/hull_adjacent_geometric_ears.md`

---

## T059 — Bounded-gate join bound

**Statement.** \(|\mathbb A_{\mathrm{join}}| \le J_M(r) = O(M^2 r^2)\) for M-gate clusters of diameter r.

**Status.** PROVED_LOCALLY (Directive 030)

**Source / proof file.** `docs/bounded_gate_join_estimate.md`

---

## T060 — Sparse unbounded-gate finite-intrusion extraction

**Statement.** \(r_n\to0\), \(M_n r_n\to0\), finite intrusion + T058 \(\Rightarrow\) signature-controlled surgery forest.

**Status.** PROVED_LOCALLY (Directive 031)

**Source / proof file.** `docs/sparse_unbounded_gate_extraction.md`

---

## T061 — Dense-gate structural trichotomy

**Statement.** Shrinking dense-gate (\(\limsup M_n r_n>0\)) sequences classify into blocks / concentration / diffuse / multicenter.

**Status.** PROVED_LOCALLY as classifier (Directive 031)

**Source / proof file.** `docs/dense_gate_trichotomy.md`

---

## T062 — Controlled dense-gate extraction

**Statement.** Ordered diffuse and finite-center dense subclasses reduce to blockwise T053B.

**Status.** PROVED_LOCALLY finite-center (Directive 032); ordered diffuse partial

**Source / proof file.** `docs/finite_center_dense_extraction.md`

---

## T063 — Dense winding concentration-compactness

**Statement.** Dense-gate sequences classify into concentrated, diffuse, or multicenter.

**Status.** PROVED_LOCALLY as classifier (Directive 032)

**Source / proof file.** `docs/dense_concentration_compactness.md`

---

## T064 — Concentrated dense-gate descent

**Statement.** Concentrated regime yields descendant cluster with fixed defect fraction at smaller scale.

**Status.** PROVED_LOCALLY for consecutive parameter blocks (Directive 032)

**Source / proof file.** `docs/recursive_dense_descent.md`

---

## T061R — Dense-gate winding-layer classification

**Statement.** Refines T061 via winding layers: concentrated descent, finite-center, diffuse nested layers, disconnected residual.

**Status.** CONJECTURAL_REFINEMENT; classifier PROVED_LOCALLY (Directive 032)

**Source / proof file.** `docs/finite_dense_gate_reduction.md`

---

## T065 — Finite-tree dense-gate reduction

**Statement.** Dense finite-intrusion sequences reduce to surgery, intrusion ray, lamination, or separate residuals.

**Status.** CONJECTURAL_TARGET (Directive 032); partial via T065R (Directive 033)

**Source / proof file.** `docs/finite_dense_gate_reduction.md`

---

## T064D — Disconnected concentration reduction

**Statement.** Disconnected spatial concentration reduces to consecutive block, finite-center T062, diffuse lamination limit, or intrusion/non-Jordan.

**Status.** PROVED_LOCALLY when consecutive block or finite-center applies (Directive 033)

**Source / proof file.** `docs/disconnected_concentration.md`

---

## T066 — Ordered lamination surgery theorem

**Statement.** ORDERED_TWO_GATE_LAMINATION admits finite cluster-surgery exhaustions with area-tight approximation.

**Status.** PROVED_LOCALLY (Directive 033)

**Source / proof file.** `docs/ordered_two_gate_lamination_surgery.md`

---

## T067 — Diffuse annular-band extraction

**Statement.** Diffuse same-sign lamination contains annular band, ordered two-gate mass, or eccentric residual.

**Status.** CONJECTURAL_GEOMETRIC_TARGET; ordered-two-gate branch PROVED_LOCALLY (Directive 033)

**Source / proof file.** `docs/diffuse_annular_band_extraction.md`

---

## T065R — Finite dense-tree lamination reduction

**Statement.** Refines T065 via T064D, T066, T067 and explicit lamination residual classes.

**Status.** CONJECTURAL_TARGET (Directive 033)

**Source / proof file.** `docs/finite_dense_lamination_reduction.md`

---

## T068 — Finite-multigate Jordan lamination surgery

**Statement.** Finite-gate Jordan laminations with measurable compatible ear selection admit area-tight surgery exhaustion.

**Status.** PROVED_LOCALLY (Directive 034)

**Source / proof file.** `docs/t068_multigate_lamination_surgery.md`

---

## T068I — Integrable-gate lamination surgery

**Statement.** T068 with \(\int m(L)^2\,d\mu<\infty\) and vanishing gate-tail signature via measurable truncations.

**Status.** PROVED_LOCALLY under explicit gate-order assumption (Directive 035)

**Source / proof file.** `docs/t068i_infinite_gate_surgery.md`

---

## T070 — Almost-everywhere gate ordering

**Statement.** \(\mathcal I(L)=0\) implies boundary and parameter order agree after null removal.

**Status.** PROVED_LOCALLY (Directive 035)

**Source / proof file.** `docs/gate_inversion_energy.md`

---

## T071 — Positive inversion structural alternative

**Statement.** Positive-inversion Jordan laminations reduce via T064D, T062, intrusion tree, or diffuse inversion residual.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; classifier partial (Directive 035)

**Source / proof file.** `docs/gate_inversion_energy.md`

---

## T072 — Parameter-disconnected reduction

**Statement.** Parameter-disconnected Jordan laminations reduce to finite blocks, disconnected concentration, intrusion tree, or diffuse component residual.

**Status.** CONJECTURAL_TARGET; partial (Directive 035)

**Source / proof file.** `docs/parameter_disconnected_laminations.md`

---

## T065I — Infinite-gate diffuse lamination reduction

**Statement.** Refines T065S via T068I and explicit infinite-gate residuals.

**Status.** CONJECTURAL_TARGET; partial (Directive 035)

**Source / proof file.** `docs/infinite_gate_diffuse_reduction.md`

---

## T073 — Finite-width positive-inversion surgery

**Statement.** Jordan laminations with \(w_\*(L)\le K\) and vanishing cross-block signature admit area-tight surgery.

**Status.** PROVED_LOCALLY (Directive 036)

**Source / proof file.** `docs/finite_width_gate_surgery.md`

---

## T073I — Summable countable-block surgery

**Statement.** Positive-inversion laminations with L1_BLOCK_SIGNATURE admit area-tight surgery exhaustion.

**Status.** PROVED_LOCALLY; clean-room verified (Directive 037)

**Source / proof file.** `docs/t073i_countable_block_surgery.md`

---

## T075 — Measurable countable monotone decomposition

**Statement.** Summable gate-order class admits measurable compatible countable monotone decomposition.

**Status.** PROVED_LOCALLY (Directive 037)

**Source / proof file.** `docs/measurable_countable_chain_selection.md`

---

## T074R — Unbounded order-width geometric reduction

**Statement.** Realizable unbounded-width gate orders force planar geometric residuals (nested ray, branching, disconnected concentration, non-Jordan limit, multicenter proliferation, or diffuse permuton).

**Status.** CONJECTURAL_TARGET; partial classifier (Directive 039)

**Source / proof file.** `docs/decreasing_orders_and_intrusion_depth.md`

---

## T076 — Nonsummable order-tail trichotomy

**Statement.** Every nonsummable positive-inversion Jordan lamination has a subsequence with concentrated, finite-center, diffuse, or infinite-intrusion/non-Jordan order interaction.

**Status.** PROVED_LOCALLY for concentrated and finite-center branches (Directive 038)

**Source / proof file.** `docs/order_interaction_concentration.md`

---

## T077-A — Bounded-depth permuton rigidity

**Statement.** Finite-intrusion Jordan gate systems with uniformly bounded depth, branching, and center count cannot converge to a genuinely diffuse gate permuton.

**Status.** PROVED_LOCALLY (Directive 039)

**Source / proof file.** `docs/bounded_depth_permuton_rigidity.md`

---

## T077 — Planar gate-permuton rigidity

**Statement.** Genuinely diffuse Jordan gate permutons from finite-intrusion noncrossing geometry force intrusion depth, branching, non-Jordan degeneration, infinite-center proliferation, or parameter-disconnected concentration.

**Status.** CONJECTURAL_RIGIDITY_TARGET; partial via T077-A (Directive 039)

**Source / proof file.** `docs/planar_gate_permuton_rigidity.md`

---

## T078 — Intrusion tree ray–branching dichotomy

**Statement.** Every infinite rooted intrusion tree has an infinite ray, arbitrarily large finite branching, or infinite local branching.

**Status.** PROVED_LOCALLY (Directive 040)

**Source / proof file.** `docs/intrusion_ray_branching_dichotomy.md`

---

## T079 — Shrinking-ray saturation

**Statement.** Shrinking intrusion ray with nested Jordan hulls and two external end gates saturates to a two-gate cluster of diameter \(O(r_j)\).

**Status.** PROVED_LOCALLY (Directive 040)

**Source / proof file.** `docs/infinite_ray_end_surgery.md`

---

## T080 — Summable infinite-ray surgery

**Statement.** Shrinking ray with SUMMABLE_RAY_SIGNATURE admits finite-tail area-tight surgery; T022 applies.

**Status.** PROVED_LOCALLY (Directive 040)

**Source / proof file.** `docs/infinite_ray_end_surgery.md`

---

## T081 — Summable branching-tree surgery

**Statement.** Locally finite intrusion tree with BRANCHING_SIGNATURE_CARLESON, Jordan-compatible finite subtree surgeries, and complete retained skeleton admits area-tight exhaustion; T022 applies.

**Status.** PROVED_LOCALLY; clean-room verified (Directive 041)

**Source / proof file.** `docs/t081_branching_tree_surgery.md`

---

## T081I — Countably branching tree surgery

**Statement.** Extend T081 to infinite local branching under CHILD_L1_SIGNATURE and global Carleson condition with two-parameter exhaustion.

**Status.** PROVED_LOCALLY; T081I_CLEAN_ROOM_VERIFIED (Directive 042)

**Source / proof file.** `docs/t081i_countable_branching_surgery.md`

---

## T082 — Infinite intrusion-tree structural reduction

**Statement.** Defect-carrying infinite intrusion trees reduce to summable ray/branching surgery, concentration, centers, positive-scale, non-Jordan, infinite-center branching, or diffuse end measure.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial via T080/T081 (Directive 041)

**Source / proof file.** `docs/infinite_tree_structural_reduction.md`

---

## T082R — Infinite intrusion-tree reduction (refined)

**Statement.** Every infinite intrusion tree reduces to T080, T081, T062/T064 descent, nonsummable ray, diffuse end measure, infinite-center branching, non-Jordan hull, parameter-disconnected, or positive-scale nonannular geometry.

**Status.** CONJECTURAL_TARGET; partial via T080/T081/T081I (Directive 042)

**Source / proof file.** `docs/infinite_local_branching_reduction.md`

---

## T082I — Infinite-tree surgery reduction

**Statement.** Every infinite intrusion tree reduces via T080, T081, T081I, concentrated/finite-center descent, nonsummable child/end geometry, infinite-center branching, non-Jordan, parameter-disconnected, or positive-scale nonannular.

**Status.** CONJECTURAL_TARGET; partial (Directive 042)

**Source / proof file.** `docs/infinite_local_branching_reduction.md`

---

## T083 — Nonsummable branching alternative

**Statement.** Branching trees failing BRANCHING_SIGNATURE_CARLESON exhibit concentrated ray, finite-center, diffuse end, infinite center, non-Jordan, parameter-disconnected, or positive-scale geometry.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; classifier partial (Directive 041)

**Source / proof file.** `docs/nonsummable_branching_residual.md`

---

## T084 — Infinite local branching alternative

**Statement.** Every countably branching intrusion tree has a subtree satisfying T081I, concentrated/finite-center child descent, nonsummable ray, diffuse end measure, infinite-center branching, non-Jordan hull, parameter-disconnected accumulation, or positive-scale nonannular geometry.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial via T081I (Directive 042)

**Source / proof file.** `docs/infinite_local_branching_reduction.md`

---

## T085 — Nonsummable ray reduction

**Statement.** Every nonsummable shrinking intrusion ray produces concentrated descent, finite-center decomposition, infinite-center geometry, annular-band geometry, non-Jordan degeneration, or a diffuse ray residual.

**Status.** PROVED_LOCALLY_CLASSIFIER (Directive 043)

**Source / proof file.** `docs/nonsummable_intrusion_rays.md`

---

## T086 — Diffuse end structural alternative

**Statement.** A nonatomic defect-carrying end measure forces spatial concentration, finite-center decomposition, infinite-center proliferation, parameter-disconnected accumulation, non-Jordan saturation, or a Cantor end residual.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial via T087 (Directive 044)

**Source / proof file.** `docs/diffuse_end_structural_theorem.md`

---

## T087 — Diffuse end-measure surgery

**Statement.** Trees with canonical end measure, point-valued spatial map a.e., END_SIGNATURE_CARLESON, and compatible antichain surgeries admit area-tight exhaustion.

**Status.** PROVED_LOCALLY; T087_CLEAN_ROOM_VERIFIED (Directive 044)

**Source / proof file.** `docs/t087_diffuse_end_surgery.md`

---

## T088 — Diffuse child-to-end promotion

**Statement.** Persistent diffuse child-center nodes promote to T087, concentrate, finite-center, infinite-center, or non-Jordan degeneration.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial (Directive 044)

**Source / proof file.** `docs/diffuse_end_structural_theorem.md`

---

## T084E — End-measure nonsummable tree reduction

**Statement.** Every tree failing T080/T081/T081I reduces via T085, T087, concentration, infinite-center, parameter-disconnected, non-Jordan, or Cantor residual.

**Status.** CONJECTURAL_TARGET; partial (Directive 044)

**Source / proof file.** `docs/nonsummable_tree_reduction.md`

---

## T089 — Finite-center non-Carleson end rigidity

**Statement.** A normalized non-Carleson tangent with Jordan hulls, point-valued spatial map, connected parameters, and finite centers must satisfy END_SIGNATURE_CARLESON after renormalization.

**Status.** CONJECTURAL_CORE_TARGET (Directive 045)

**Source / proof file.** `docs/finite_center_end_rigidity.md`

---

## T090 — Frostman end-surgery criterion

**Statement.** Dimensional inequality on \(m(v)\) vs \(\Phi(v)\) implies END_SIGNATURE_CARLESON.

**Status.** CONJECTURAL_TARGET (Directive 045)

**Source / proof file.** `docs/frostman_end_surgery_criterion.md`

---

## T086R — Non-Carleson diffuse-end reduction

**Statement.** Nonatomic end measures failing T087 reduce via bad-cylinder tangents to solved routes or NONCARLESON_CANTOR_END_TANGENT.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial (Directive 045)

**Source / proof file.** `docs/noncarleson_diffuse_end_reduction.md`

---

## T084C — Cantor-end tree reduction

**Statement.** Trees failing T080/T081I/T087 reduce via T085, T086R, or global residuals.

**Status.** CONJECTURAL_TARGET; partial (Directive 045)

**Source / proof file.** `docs/noncarleson_diffuse_end_reduction.md`

---

## T089R — Finite-center endpoint-correspondence rigidity

**Statement.** Normalized bad tangent with nested Jordan hulls, measurable compact-valued \(\Phi\), connected parameters, finite incidence-center complexity, \(\mu_+(E_+)=0\), and no degeneration satisfies renormalized end-Carleson.

**Status.** CONJECTURAL_CORE_TARGET (Directive 047; first gap: strict packing)

**Source / proof file.** `docs/finite_center_singleton_rigidity.md`

---

## T090R — Correspondence Frostman criterion

**Statement.** Set-valued cylinder Frostman inequality on \(m(v)\) vs \(\Psi_{\mathrm{geom}}(v)\) implies END_SIGNATURE_CARLESON; positive-diameter component via T091.

**Status.** CONJECTURAL_TARGET; critical scaling open (Directive 047)

**Source / proof file.** `docs/singleton_end_frostman_criterion.md`

---

## T091 — Continuum-end positive-scale reduction

**Statement.** Positive-diameter nested Jordan ends have positive limiting spatial scale; route to annular, finite-center, nonannular, or degeneration geometry.

**Status.** PROVED_LOCALLY_CLASSIFIER (Directive 046)

**Source / proof file.** `docs/continuum_end_positive_scale_reduction.md`

---

## T092 — Endpoint correspondence dichotomy

**Statement.** Every normalized non-Carleson tangent has singleton a.e., positive-diameter mass, incompatible nesting, non-Jordan degeneration, or graph compactness failure.

**Status.** PROVED_LOCALLY_CLASSIFIER (Directive 046)

**Source / proof file.** `docs/endpoint_repaired_noncarleson_reduction.md`

---

## T086E — Endpoint-repaired non-Carleson reduction

**Statement.** Nonatomic end measures failing T087 reduce via incidence routes, T091 continuum geometry, or `NONCARLESON_SINGLETON_CANTOR_END_TANGENT`.

**Status.** CONJECTURAL_TARGET; partial (Directive 046)

**Source / proof file.** `docs/endpoint_repaired_noncarleson_reduction.md`

---

## T086S — Singleton Cantor-end reduction

**Statement.** Every non-Carleson singleton Cantor tangent routes via concentration, finite-center, T089R, T090R, degeneration, infinite-center, or exact critical residual.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial (Directive 047)

**Source / proof file.** `docs/singleton_cantor_end_reduction.md`

---

## T084S — Singleton-end tree reduction

**Statement.** Every tree not covered by T080/T081/T081I/T085/T087 reduces via T086S, T091 continuum geometry, or global residuals.

**Status.** CONJECTURAL_TARGET; partial (Directive 047)

**Source / proof file.** `docs/singleton_cantor_end_reduction.md`

---

## T093 — Multigeneration signature packing

**Statement.** Under singleton shrinking Jordan hypotheses, \(P_L(v)\le(1-\eta)\Phi(v)\) for bounded \(L\) and \(\eta>0\).

**Status.** PROVED_LOCALLY (Directive 048)

**Source / proof file.** `docs/multigeneration_signature_packing.md`

---

## T094 — Critical equality rigidity

**Statement.** Every Jordan-realizable singleton equality tangent routes to T087, concentration, finite-center, annular/thin, or degeneration.

**Status.** CONJECTURAL_RIGIDITY_TARGET (Directive 049)

**Source / proof file.** `docs/t094_critical_equality_rigidity.md`

---

## T094-A — Equality-core tangent theorem

**Statement.** Every deep neutral-corona sequence has, after subsequence selection, contraction (T095), concentration/finite-center, bad residual, or a positive-signature tangent satisfying the complete equality ledger.

**Status.** CONJECTURAL_REPAIRED_TARGET (Directive 050); first gap at signature-weighted pruning + semicontinuity

**Source / proof file.** `docs/t094a_equality_core_tangent.md`

---

## T095 — Deficit-to-contraction

**Statement.** Persistent cumulative deficit \(\mathfrak D_L(v)\ge\epsilon\Phi(v)\) with controlled boundary implies \(P_L(v)\le(1-\eta(\epsilon))\Phi(v)\).

**Status.** CONJECTURAL_DEFICIT_TARGET (Directive 050)

**Source / proof file.** `docs/deficit_to_multigeneration_contraction.md`

---

## T096 — Positive-signature equality-core extraction

**Statement.** Long neutral coronas with \(\mathfrak D_L=o(\Phi)\) contain a coherent positive-signature subtree of unbounded depth with uniformly vanishing normalized deficits.

**Status.** CONJECTURAL_SELECTION_TARGET (Directive 050)

**Source / proof file.** `docs/tree_equality_core_selection.md`

---

## T097 — Exact neutral-state transfer

**Statement.** Admissible neutral singleton-end nodes admit augmented-state decomposition with compact certified transfer family; nonclosed scalar deficits appear as state coordinates.

**Status.** CONJECTURAL_STATE_TARGET (Directive 051)

**Source / proof file.** `docs/neutral_transfer_operators.md`

---

## T098 — Neutral Bellman contraction

**Statement.** Positive homogeneous Bellman potential comparable to \(\Phi_{\mathrm{end}}\) yields multigeneration contraction without requiring small individual ledger deficits.

**Status.** CONJECTURAL_CORE_TARGET (Directive 051)

**Source / proof file.** `docs/t098_neutral_bellman_contraction.md`

---

## T099 — Critical state rigidity

**Statement.** Invariant zero-slack state measures route to solved branches or explicit diffuse critical residual.

**Status.** CONJECTURAL_RIGIDITY_TARGET (Directive 051)

**Source / proof file.** `docs/t099_critical_state_rigidity.md`

---

## T100 — Neutral transition escape classification

**Statement.** Every admissible neutral transition subsequence routes to a geometric branch, removable coboundary, or compact-core convergence.

**Status.** PROVED_LOCALLY on tested fixture (Directive 052)

**Source / proof file.** `docs/neutral_escape_profile_classification.md`

---

## T097C — Compactified neutral-state transfer

**Statement.** Neutral transitions route or belong to sequentially compact \(\mathscr A_{\mathrm{core}}\) with closed limit recursion.

**Status.** CONJECTURAL_CORE_TARGET (Directive 052)

**Source / proof file.** `docs/t097c_compactified_state_transfer.md`

---

## T098C — Compact-core Bellman alternative

**Statement.** On \(\mathscr A_{\mathrm{core}}\), either certified Bellman contraction or critical invariant measure.

**Status.** CONJECTURAL_DUALITY_TARGET (Directive 052); NOT_APPLICABLE on empty core; retired if T102 universal

**Source / proof file.** `docs/compact_core_bellman_duality.md`

---

## T101 — Admissible neutral transition exhaustion

**Statement.** Every realizable neutral singleton-end transition satisfies a routing predicate covering concentration, positive scale, branching, center, gate, parameter, non-Jordan, or coboundary reduction.

**Status.** PROVED_FINITE_DOMAIN (Directive 053); universal infinite-dimensional closure open

**Source / proof file.** `docs/neutral_transition_routing_ledger.md`

---

## T102 — Empty neutral-core theorem

**Statement.** \(\mathscr A_{\mathrm{core}}=\varnothing\) under singleton shrinking Jordan hypotheses.

**Status.** PROVED_FINITE_DOMAIN (Directive 053)

**Source / proof file.** `docs/empty_neutral_core_theorem.md`

---

## T103 — Coherent route extraction

**Statement.** Deep neutral coronas admit coherent single-branch subsystems, T093 contraction, or explicit global residual.

**Status.** CONJECTURAL_SELECTION_TARGET (Directives 053–055); deferred until T105R universal closure

**Source / proof file.** `docs/coherent_route_subsystem_selection.md`

---

## T089E — Empty-core singleton-end reduction

**Statement.** T101–T103 eliminate the independent neutral singleton Cantor residual.

**Status.** CONJECTURAL_REDUCTION_TARGET (Directive 053); universal version open (Directive 054)

**Source / proof file.** `docs/empty_core_singleton_reduction.md`

---

## T104 — Countable-child transition exhaustion

**Statement.** Every countably branching neutral transition routes to T081I, concentration, center, parameter, non-Jordan, or positive-scale branches.

**Status.** PROVED_LOCALLY on tested fixture (Directives 054–055; revalidated with augmented order datum)

**Source / proof file.** `docs/countable_child_transition_exhaustion.md`

---

## T105 — Measure-valued transition closure

**Statement.** Bounded coercive moment transitions are sequentially compact with closed recursion.

**Status.** Superseded by T105R (Directive 055); original gate-order component NOT_CLOSED (Directive 054)

**Source / proof file.** `docs/measure_transition_tightness_and_closure.md`

---

## T105R — Gate-order-augmented measure transition closure

**Statement.** Augmented transitions \((\Pi_v,\Omega_v,\Lambda_v)\) are sequentially compact with closed recursion under coercive moments.

**Status.** PROVED_LOCALLY on tested fixture (Directive 055); universal version CONJECTURAL

**Source / proof file.** `docs/t105r_measure_transition_closure.md`

---

## T107 — Weakly closed gate-order measure representation

**Statement.** Finite/countable gate transitions admit seam-independent \((\Pi_v,\Omega_v,\Lambda_v)\) with controlled total variation and collision routing.

**Status.** PROVED_LOCALLY on tested fixture (Directive 055)

**Source / proof file.** `docs/marked_cyclic_gate_measures.md`

---

## T108 — Order-augmented infinite transition exhaustion

**Statement.** Every augmented infinite-dimensional neutral transition routes to a solved branch or explicit residual.

**Status.** CONJECTURAL_EXHAUSTION_TARGET (Directive 055); T104/T106 revalidated locally

**Source / proof file.** `docs/order_augmented_infinite_exhaustion.md`

---

## T106 — Unbounded gate-complexity exhaustion

**Statement.** Unbounded gate/order complexity routes to T073I, finite-center, infinite intrusion, infinite-center, parameter disconnection, non-Jordan, or positive-scale.

**Status.** PROVED_LOCALLY on tested fixture (Directives 054–055; revalidated with \(\Pi_v,\Omega_v,\Lambda_v\))

**Source / proof file.** `docs/unbounded_gate_transition_exhaustion.md`

---

## T101-U — Universal transition exhaustion

**Statement.** Every admissible neutral singleton-end transition routes to a solved or explicit residual branch.

**Status.** CONJECTURAL_UNIVERSAL_EXHAUSTION (Directive 054)

**Source / proof file.** `docs/universal_infinite_transition_exhaustion.md`

---

## T102-U — Universal empty neutral-core theorem

**Statement.** \(\mathscr A_{\mathrm{res}}=\varnothing\) after routing; no independent neutral transition type survives.

**Status.** CONJECTURAL_UNIVERSAL_CORE_TARGET (Directive 054)

**Source / proof file.** `docs/infinite_dimensional_empty_core_reduction.md`

---

## T089R — Singleton end rigidity (closure chain)

**Statement.** T093 coverage + T094 close NONCARLESON_SINGLETON_CANTOR_END_TANGENT.

**Status.** CONJECTURAL_CORE_TARGET (Directive 049)

**Source / proof file.** `docs/t089r_singleton_end_rigidity.md`

---

## T086M — Multigeneration singleton-end reduction

**Statement.** Every singleton shrinking non-Carleson tangent routes via T093, solved branches, or exact critical equality model.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial (Directive 048)

**Source / proof file.** `docs/multigeneration_singleton_end_rigidity.md`

---

## T084R — Nonsummable child and end reduction

**Statement.** Every tree failing T080/T081/T081I admits a subtree in one of the T085/T086 residual classes or explicit non-tree geometry.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; partial classifier (Directive 043)

**Source / proof file.** `docs/nonsummable_tree_reduction.md`

---

## T082F — Infinite-tree final reduction

**Statement.** Every infinite intrusion tree is surgically closed via T080/T081/T081I or belongs to an exact T084R residual class.

**Status.** CONJECTURAL_TARGET; partial (Directive 043)

**Source / proof file.** `docs/infinite_tree_final_reduction.md`

---

## T072C — Nonsummable parameter-component reduction

**Statement.** Parameter-disconnected laminations with nonsummable component interactions reduce via T076, infinite intrusion, genuinely diffuse permuton, or non-Jordan behavior.

**Status.** CONJECTURAL_TARGET; partial (Directive 038)

**Source / proof file.** `docs/permuton_level_diffuse_reduction.md`

---

## T065P — Permuton-level diffuse reduction

**Statement.** Diffuse finite-intrusion Jordan laminations reduce via existing surgery, T076 descent, intrusion/branching, non-Jordan geometry, or genuinely diffuse permuton residual.

**Status.** CONJECTURAL_TARGET; partial (Directive 038)

**Source / proof file.** `docs/permuton_level_diffuse_reduction.md`

---

## T065PR — Diffuse permuton residual elimination

**Statement.** Every finite-intrusion Jordan-hull diffuse gate sequence reduces to T073I, T076 descent, intrusion/branching, infinite-center, parameter-disconnected, non-Jordan hull, or positive-scale nonannular geometry; no independent bounded-depth diffuse permuton.

**Status.** CONJECTURAL_TARGET; partial via T077-A (Directive 039)

**Source / proof file.** `docs/diffuse_permuton_residual_elimination.md`

---

## T072S — Summable parameter-component reduction

**Statement.** Parameter-disconnected laminations with summable component geometry satisfy T073I.

**Status.** CONJECTURAL_TARGET; partial (Directive 037)

**Source / proof file.** `docs/countable_order_diffuse_reduction.md`

---

## T065C — Countable-order diffuse reduction

**Statement.** Refines T065O via T073I and explicit nonsummable/unbounded residuals.

**Status.** CONJECTURAL_TARGET; partial via T073I (Directive 037)

**Source / proof file.** `docs/countable_order_diffuse_reduction.md`

---

## T074 — Noncrossing order-width theorem

**Statement.** Unbounded monotone width in noncrossing Jordan laminations forces planar geometric residuals.

**Status.** CONJECTURAL_STRUCTURAL_TARGET; classifier partial (Directive 036)

**Source / proof file.** `docs/noncrossing_order_width.md`

---

## T071R — Positive-inversion order classification

**Statement.** Refines T071 via monotone width, summable blocks, T074, permuton residuals.

**Status.** CONJECTURAL_REFINEMENT; classifier partial (Directive 036)

**Source / proof file.** `docs/positive_inversion_order_classification.md`

---

## T072R — Parameter-support order reduction

**Statement.** Parameter-disconnected Jordan laminations reduce via finite-width surgery or explicit residuals.

**Status.** CONJECTURAL_TARGET; partial (Directive 036)

**Source / proof file.** `docs/parameter_support_order_reduction.md`

---

## T065O — Order-theoretic diffuse reduction

**Statement.** Diffuse Jordan laminations reduce via T066–T073/T073I or order/intrusion/center residuals.

**Status.** CONJECTURAL_TARGET; partial via T073 (Directive 036)

**Source / proof file.** `docs/order_theoretic_diffuse_reduction.md`

---

## T069 — Thin eccentric lamination surgery

**Statement.** THIN_LEAF_ORDERED laminations with width-signature summability admit area-tight surgery.

**Status.** PROVED_LOCALLY (Directive 034)

**Source / proof file.** `docs/t069_thin_eccentric_surgery.md`

---

## T067R — Thick/thin/multigate diffuse alternative

**Statement.** Diffuse lamination reduces to T066, T068, T069, thick band, or explicit residual.

**Status.** PROVED_LOCALLY as classifier (Directive 034)

**Source / proof file.** `docs/thick_thin_multigate_alternative.md`

---

## T065S — Diffuse lamination surgery reduction

**Statement.** Diffuse finite-tree laminations reduce via T066/T068/T069/annular or explicit residuals.

**Status.** CONJECTURAL_TARGET; partial via T068/T069 (Directive 034)

**Source / proof file.** `docs/diffuse_lamination_residuals.md`

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

**Status.** PROVED_LOCALLY for \(\mathcal D_{\mathrm{nest}}^{\mathrm{ann}}\) (T036-N1-ANN)

**Source / proof file.** `docs/nested_lobe_controlled_bridge.md`, `docs/t036_n1_annular_proof.md`

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

