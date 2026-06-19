# Spectral Axiom Ledger (Directive 003)

Primary sources audited (exact arXiv versions as specified):

| ID | Paper | Version |
|----|-------|---------|
| GL24 | Greene–Lobb, *Rectangles inscribed in rectifiable Jordan curves* | arXiv:2404.05179 (latest in cache) |
| GL24b | Greene–Lobb, *Isosceles trapezoids* | arXiv:2407.07798 (latest in cache) |
| GL26 | Greene–Lobb, *Spectral invariants and the square peg problem* | arXiv:2604.17116v1 |
| AI24 | Asano–Ike, *The rectifiable rectangular peg problem* | arXiv:2412.21057v3 |

Legend for columns: **LP** = used as Level-F LP constraint; **Geom** = geometric interpretation only; **C⁰** = survives C⁰ limit of smooth approximants (as stated in source).

Notation follows sources exactly. **Inferred** properties are marked separately.

---

## Maintenance

**M001** (nonblocking): Classify rank-≤4 edge-quadruple square systems. Current benchmark corpus (`data/benchmark_polygons.json`, 5 polygons): **no rank-≤4 unsupported systems observed**; all quadruples either yield rank-6 isolated solutions or rank-5 families. Future adversarial polygon runs must not silently classify rank-≤4 systems as empty.

---

## 1. Endpoint values

| Property | Statement | Notation | Reference | Regularity | ℓ₁/ℓ₂ | C⁰ | Curve class | LP | Geom |
|----------|-----------|----------|-----------|------------|-------|-----|-------------|-----|------|
| P1a | ℓ(γ, 0) = 0 | ℓ(γ, θ), θ ∈ [0, π] | GL26 §1, bullet list | Smooth (extends to limits) | ℓ₂ main | Yes | Smooth → rectifiable/locally monotone via limits | Yes | No |
| P1b | ℓ(γ, π) = Area(γ) | A(γ) | GL26 §1; GL24 §4 | As above | ℓ₂ | Yes | As above | Yes (g(1)=1 normalized) | No |

**Assumptions.** Jordan Floer spectral invariant for isosceles trapezoids (homological degree 2, aspect ratio β); GL24 rectangle case uses ℓ(γ, θ) for rectangles.

---

## 2. Area bounds

| Property | Statement | Notation | Reference | Regularity | ℓ₁/ℓ₂ | C⁰ | Curve class | LP | Geom |
|----------|-----------|----------|-----------|------------|-------|-----|-------------|-----|------|
| P2a | 0 ≤ ℓ(γ, θ) ≤ Area(γ) for all θ | — | GL26 §1 Monotonicity range | Smooth | ℓ₂ | Yes | Smooth + limits | Yes (0≤g≤1) | No |
| P2b | B(γ) := Area(γ)/Rad(γ)² ≤ π (isodiametric) | B(γ), Rad(γ) | GL26 §2; standard | Jordan | — | Yes | All Jordan | Normalization only | Yes |
| P2c | Scholium: μ(S(γ) ∩ [0, π/k]) ≥ B(γ)/k | S(γ) = {θ : ℓ′(γ,θ) exists, ℓ′>0} | GL26 Scholium 2.3 | Jordan (limit of smooth) | ℓ₂ | Yes | Jordan | No (measure) | Yes |

---

## 3. Monotonicity

| Property | Statement | Notation | Reference | Regularity | ℓ₁/ℓ₂ | C⁰ | Curve class | LP | Geom |
|----------|-----------|----------|-----------|------------|-------|-----|-------------|-----|------|
| P3a | θ ↦ ℓ(γ, θ) is **monotone increasing** | — | GL26 §1; GL24b §3 | Smooth; continuous extension | ℓ₂ | Yes | Smooth → broader classes | Yes | No |
| P3b | θ ↦ ℓ(γ, θ) is a **bijection** [0, π] → [0, A(γ)] | — | GL26 §1 (smooth setting) | Smooth generic | ℓ₂ | Open | Smooth generic | **Inferred** (open condition) | No |

**Note.** Strict monotonicity is used heuristically but is an open dense condition for smooth curves, not a closed LP constraint. Nondecreasing is the proved closure property.

---

## 4. Strictness / bijectivity

| Property | Status | Reference |
|----------|--------|-----------|
| Strict increase on smooth generic | **Inferred** from open dense regularity | GL26 §1 |
| Bijection | Stated for smooth setting | GL26 §1 |

Not encoded as hard LP unless δ-gap family is run separately.

---

## 5. Continuity

| Property | Statement | Reference | Regularity | C⁰ | LP |
|----------|-----------|-----------|------------|-----|-----|
| P5 | θ ↦ ℓ(γ, θ) is continuous on [0, π] | GL24b §3; limits in GL26 Thm B proof | Rectifiable / locally monotone after limit | Yes | Implied by Lipschitz |

---

## 6. Lipschitz continuity

| Property | Statement | Notation | Reference | Regularity | ℓ₁/ℓ₂ | C⁰ | LP |
|----------|-----------|----------|-----------|------------|-------|-----|-----|
| P6 | \|ℓ(γ, θ₁) − ℓ(γ, θ₂)\| ≤ Rad(γ)² · Area(γ)⁻¹ · \|θ₁ − θ₂\| | Rad(γ), Area(γ) | GL26 §1; GL24b Prop. 3.5 | Smooth; persists in limit | ℓ₂ | Yes | Yes (κ=π/B) |

Normalized: |g(y) − g(x)| ≤ κ|y − x| with κ = π/B = πR²/A.

---

## 7. Triangle inequality (subadditivity)

| Property | Statement | Notation | Reference | Regularity | ℓ₁/ℓ₂ | C⁰ | LP |
|----------|-----------|----------|-----------|------------|-------|-----|-----|
| P7 | ℓ(γ, θ₁ + θ₂) ≤ ℓ(γ, θ₁) + ℓ(γ, θ₂) when θ₁+θ₂ ≤ π | — | GL26 §1; GL24b Prop. 3.6 | Smooth | ℓ₂ | Yes | Yes |

---

## 8. Spectrality

| Property | Statement | Reference | Regularity | ℓ₁/ℓ₂ | LP | Geom |
|----------|-----------|-----------|------------|-------|-----|------|
| P8 | ∃ inscribed θ-trapezoid P with ℓ(γ, θ) = Area(P) | GL26 §1 | Smooth | ℓ₂ | No (Level S) | Yes |

---

## 9. Derivative property

| Property | Statement | Reference | Regularity | ℓ₁/ℓ₂ | LP | Geom |
|----------|-----------|-----------|------------|-------|-----|------|
| P9 | For a.e. θ, ℓ is differentiable and ℓ′(γ, θ) = R(P)² for spectral rectangle/trapezoid P | GL26 Thm 5.1 | Smooth (dense open) | ℓ₂ | No (Level S/G) | Yes |

---

## 10. Duality (two invariants — **indexed, not self-dual**)

| Property | Statement | Notation | Reference | Regularity | LP |
|----------|-----------|----------|-----------|------------|-----|
| P10 | ℓ(γ, θ, **α**) + ℓ(γ, π − θ, **β**) = Area(γ) | α, β = aspect-ratio parameters; ℓ(γ,θ) := ℓ(γ,θ,**β**) | GL24 §4.1; GL24b | Smooth rectangles / trapezoids | Two-invariant model only |

**Critical warning (Directive 003).** Do **not** encode ℓ(θ) + ℓ(π − θ) = A for a **single** invariant unless a source proves it. The proved relation pairs **α** and **β** indices.

Normalized two-invariant duality at grid x_i = i/N:

\[
g_1(x_i) + g_2(1 - x_i) = 1.
\]

---

## 11. Continuity under variation of the curve

| Property | Statement | Reference | C⁰ |
|----------|-----------|-----------|-----|
| P11a | ℓ(γₙ, θ) → ℓ(γ, θ) when γₙ → γ uniformly (rectifiable/locally monotone) | GL26 Thm B proof; GL24b | Yes |
| P11b | Spectral rectangles converge to limit set (possibly collapsed) | GL26 §1 shrinkout discussion | — |

---

## 12. Hofer-distance / variation bounds

| Property | Statement | Reference | LP |
|----------|-----------|-----------|-----|
| P12 | Action variation in θ bounded by Rad²/Area (Lipschitz constant above) | GL24b Prop. 3.5 | Yes (same as P6) |

---

## 13. Rectifiable non-shrinkout lemma

| Property | Statement | Reference | Regularity |
|----------|-----------|-----------|------------|
| P13 | If lim_{θ→π} ℓ₂(γ,r,θ) ≠ 0 then trapezoids of angle θ exist for θ in (0,π) | GL24b Thm B | Rectifiable / locally monotone |

Level G — not in Level-F LP.

---

## 14. Positive-measure rectangle theorem

| Property | Statement | Reference |
|----------|-----------|-----------|
| P14 | For rectangles in smooth curves, positive measure of θ with spectral contribution | GL24 / AI24 framework |

Level S/G.

---

## 15. Asano–Ike lift condition and diagonal obstruction

| Property | Statement | Reference | LP |
|----------|-----------|-----------|-----|
| P15a | Microlocal lift for rectangle spectral invariants on rectifiable curves | AI24 v3 | No |
| P15b | Diagonal exclusions prevent interpreting limit as nondegenerate rectangle | GL24 shrinkout; AI24 | No (Level G) |

---

## Level classification summary

| Level | Properties |
|-------|------------|
| **F** | P1, P3 (monotone), P6, P7, P10 (two-invariant only) |
| **S** | P8, P9, barcode/Floer grading |
| **G** | P13, P15, derivative = squared radius, Z₄ symmetry |

---

## Inferred / conjectural (not source theorems)

| ID | Statement | Status |
|----|-----------|--------|
| I1 | Positive midpoint spectral density m(γ,ℓ)>0 at θ=π/2 | **CONJECTURAL** (Midpoint Nonflatness) |
| I2 | Level-F axioms force m>0 | **DISPROVED** for κ > κ_c ≈ 1.026 (see Directive 003 report) |
| I3 | ℓ(θ)+ℓ(π−θ)=A for single invariant | **NOT IN SOURCE** — do not use |
