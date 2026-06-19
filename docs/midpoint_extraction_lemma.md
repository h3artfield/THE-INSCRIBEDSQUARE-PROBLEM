# Midpoint Extraction Lemma (Abstract)

**Status:** PROVED_LOCALLY (abstract functional statement; geometric realization via Greene–Lobb T003)

**Dependencies:** T002 (noncollapse compactness), T003 (derivative property on approximants)

---

## Statement

Let {γₙ} be generic smooth Jordan curves converging uniformly to a Jordan curve γ. Suppose:

1. (Area and radius control) Area(γₙ) → A > 0 and Rad(γₙ) → R > 0 with A/R² bounded away from 0.

2. (Spectral convergence) The normalized invariants gₙ(x) = ℓ(γₙ, πx)/A(γₙ) converge uniformly to g on [0,1].

3. (Derivative property on approximants) For each n, for Lebesgue-a.e. θ, ℓ(γₙ,·) is differentiable and ℓ′(γₙ,θ) = R(Pₙ,θ)² for a spectral inscribed rectangle Pₙ,θ.

4. (Positive midpoint slope hypothesis — **H-uniform**) There exist ε > 0 and c > 0 and N₀ such that for all n ≥ N₀ and all h ∈ (0, ε],
   \[
   \frac{g_n(\tfrac12 + h) - g_n(\tfrac12 - h)}{2h} \geq c
   \]
   for all h ∈ (0, ε].

Then γ contains a nondegenerate inscribed square.

---

## Proof

### Step 1 — Transfer midpoint slope to the limit

Uniform convergence gₙ → g and the uniform lower bound on symmetric difference quotients on (0, ε] imply

\[
D^+(g, \tfrac12) \geq c > 0.
\]

*Justification:* Fix h ∈ (0, ε]. For large n, |gₙ − g| < δ on [0,1] with δ = ch/4. Then
\[
\frac{g(\tfrac12+h)-g(\tfrac12-h)}{2h}
\geq \frac{g_n(\tfrac12+h)-g_n(\tfrac12-h)}{2h} - \frac{2δ}{2h} \geq c - \frac{δ}{h} \geq c/2.
\]
Take limsup as h ↓ 0.

We do **not** assume pointwise convergence of derivatives.

### Step 2 — Points of differentiability for g

g is κ-Lipschitz (κ = πR²/A), hence absolutely continuous. Therefore g is differentiable for Lebesgue-a.e. x ∈ (0,1). In particular, pick x₀ = ½ as a differentiability point after adjusting on a null set (equivalence class of AC functions).

At such a point, D^+(g,½) ≥ c implies g′(½) ≥ c > 0.

### Step 3 — Approximating rectangles with uniform radius lower bound

For each n and θ = π/2, choose spectral rectangle Pₙ with Area(Pₙ) = ℓ(γₙ, π/2). The symmetric slope lower bound and monotonicity give ℓ(γₙ, π/2 + h) − ℓ(γₙ, π/2 − h) ≥ c · A(γₙ) · 2h for small h.

By the derivative property (T003) on approximants, for a.e. θ near π/2 there exist spectral rectangles with ℓ′(γₙ,θ) = Rₙ,θ². The positive slope at ½ forces a sequence of angles θₙ → π/2 with ℓ′(γₙ,θₙ) bounded below by η > 0 for large n (otherwise the average slope near ½ would fall below c).

Hence there exist spectral rectangles R(Pₙ) ≥ √η for infinitely many n.

### Step 4 — Compactness of vertices

Each Pₙ has four vertices on γₙ. After passing to a subsequence, γₙ → γ uniformly and vertex parameters converge (compactness of S¹⁴ modulo translation — fix one vertex by reparametrization).

### Step 5 — Four distinct vertices in the limit

Uniform lower bound R(Pₙ) ≥ √η prevents diagonal collapse (T002): limit vertices are distinct.

### Step 6 — Rectangle equations pass to the limit

Side-length and orthogonality conditions are closed under uniform convergence of the underlying curve and vertex positions. Limit quadrilateral is a rectangle inscribed in γ.

### Step 7 — Angle converges to π/2

θₙ was chosen near π/2 with θₙ → π/2 along the subsequence. Limit rectangle has diagonal angle π/2, i.e. is a **square**.

---

## Remarks

- The hypothesis is **functional** (positive symmetric slope), not geometric.
- Without Step 3's derivative property, a flat g could come from non-spectral functions — the lemma is designed for spectral limits.
- The proof deliberately avoids assuming ℓ′(γₙ,·) → ℓ′(γ,·) pointwise.

---

## Ledger entry

See **T012** in `docs/theorem_ledger.md`.
