# Missing Axiom Candidates

Goal: identify the weakest additional statement forcing positive midpoint density D⁺(g, ½) > 0.

Status labels: `SOURCE_THEOREM` | `DERIVED` | `CONJECTURAL` | `NUMERICAL_ONLY` | `DISPROVED`

---

## Tested in Directive 003

| # | Candidate | Status | Result |
|---|-----------|--------|--------|
| — | Level F only (endpoints, monotone, κ-Lipschitz, subadditivity) | SOURCE_THEOREM fragments | **DISPROVED** as forcing D⁺>0 for κ > κ_c ≈ 1.026 |
| — | Indexed duality g₁(x)+g₂(1−x)=1 | SOURCE_THEOREM (GL24 §4.1) | **No improvement** vs one-invariant for κ ≥ 11/10 |
| — | Strict monotonicity gap δ>0 | NUMERICAL_ONLY | δ→0 recovers nondecreasing threshold; see sweep `strict_delta_1e4` |

---

## Not yet forcing (candidates for future)

| # | Candidate | Status | Notes |
|---|-----------|--------|-------|
| 1 | Semiconcavity of g | CONJECTURAL | Not in GL26 Level-F |
| 2 | Concavity of g | CONJECTURAL | Conflicts with countermodels (PL with flat middle) |
| 3 | Midpoint convexity g(½) ≤ (g(½−h)+g(½+h))/2 | CONJECTURAL | Would force D⁺>0; not proved for spectral invariants |
| 4 | Strict subadditivity g(x+y) < g(x)+g(y) on some set | CONJECTURAL | Too strong; not expected globally |
| 5 | Quantitative triangle gap | CONJECTURAL | Scholium gives measure lower bound, not pointwise |
| 6 | Lower bound on local total variation | CONJECTURAL | Related to Scholium 2.3 |
| 7 | Ordering g₁ ≤ g₂ or vice versa | CONJECTURAL | Not sourced |
| 8 | Barcode length lower bound | CONJECTURAL | Level S |
| 9 | Spectral gap condition | CONJECTURAL | Level S |
| 10 | Z₄-equivariant square-angle constraints | CONJECTURAL | Level G |
| 11 | Lower semicontinuity under curve approximation | SOURCE_THEOREM (partial) | Does not force midpoint mass |
| 12 | Exclusion of action on diagonal | CONJECTURAL | Level G (AI24 / shrinkout) |

---

## Weakest plausible forcing package (hypothesis)

Combine **Level S** (derivative property P9 on a positive-measure set) with **Scholium 2.3** (P2c) to deduce a **measure-theoretic** lower bound on ∫_{|θ−π/2|<ε} ℓ′(θ) dθ, then derive pointwise D⁺>0 via Lebesgue differentiation — **not completed** in Directive 003.

**Next theorem target:** Prove that for every Jordan curve γ, the **actual** spectral invariant (not merely Level-F) satisfies D⁺(g, ½) > 0, or produce a Jordan curve whose spectral invariant violates it while satisfying all **Level S** axioms.

---

## Maintenance M001

**Classify rank-≤4 edge-quadruple square systems.**

Benchmark scan (5 polygons): **no feasible rank-≤4 unsupported systems found.** No simple-polygon rank-≤4 example in current corpus. Do not implement full classifier until a concrete case appears.
