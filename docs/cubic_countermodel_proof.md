# Cubic Countermodel — Analytic Proof

**Function:**

\[
g_*(x) = 4x^3 - 6x^2 + 3x = 4\left(x-\tfrac12\right)^3 + \tfrac12.
\]

**Status:** PROVED (exact symbolic + independent rational verification)

---

## 1. Endpoints

\[
g_*(0) = 0, \qquad g_*(1) = 4 - 6 + 3 = 1.
\]

Centered form: expand \(4(x-\tfrac12)^3 + \tfrac12 = 4x^3 - 6x^2 + 3x\). ✓

---

## 2. Strict monotonicity

\[
g_*'(x) = 12x^2 - 12x + 3 = 3(2x-1)^2 \ge 0,
\]

with equality **only** at \(x = \tfrac12\).

For \(0 \le x < y \le 1\):

\[
g_*(y) - g_*(x) = \int_x^y 3(2t-1)^2\, dt > 0,
\]

since \(3(2t-1)^2 \ge 0\) and cannot vanish on a nontrivial interval \([x,y]\) (it vanishes only at the isolated point \(t=\tfrac12\), which has measure zero).

**Distinction:**

| Property | Status |
|----------|--------|
| \(g_*\) strictly increasing | Yes |
| \(g_*\) strictly increasing bijection \([0,1]\to[0,1]\) | Yes |
| \(g_*'\) strictly positive everywhere | No (vanishes at \(x=\tfrac12\)) |
| \(g_*'\) positive almost everywhere | Yes |

---

## 3. Lipschitz constant

On \([0,1]\), \(g_*'\) is a quadratic opening upward with minimum \(0\) at \(x=\tfrac12\) and endpoint values \(g_*(0)=g_*(1)=3\). Hence

\[
0 \le g_*(x) \le 3, \qquad \operatorname{Lip}(g_*) = 3.
\]

Level-F Lipschitz constraint \(|g(y)-g(x)| \le \kappa|y-x|\) holds for every **\(\kappa \ge 3\)**.

**No claim** for \(1 < \kappa < 3\).

---

## 4. Continuum subadditivity

For \(x,y \ge 0\), \(x+y \le 1\):

\[
H(x,y) = g_*(x) + g_*(y) - g_*(x+y) = 12xy(1-x-y).
\]

**Proof:** Expand both sides; factorization verified symbolically (SymPy) and rationally (sample points).

Since \(x,y,1-x-y \ge 0\) on the triangle \(T\), \(H(x,y) \ge 0\).

**Equality loci:** \(x=0\), \(y=0\), or \(x+y=1\).

At \((x,y)=(\tfrac12,\tfrac12)\): \(H=12\cdot\tfrac14\cdot\tfrac12\cdot 0 = 0\) — equality with **interior** points (not only boundary).

---

## 5. Midpoint density

\[
g_*\left(\tfrac12\right)=\tfrac12,\qquad g_*'\left(\tfrac12\right)=0.
\]

The collapse signature is the **vanishing derivative**, not \(g_*(1/2)=0\).

For \(0<h<\tfrac12\):

\[
g_*\left(\tfrac12+h\right) = \tfrac12 + 4h^3, \qquad
g_*\left(\tfrac12-h\right) = \tfrac12 - 4h^3.
\]

Hence

\[
D_h(g_*) = \frac{4h^3 - (-4h^3)}{2h} = 4h^2 \to 0 \quad (h \downarrow 0),
\]

so \(D^+(g_*,\tfrac12) = D^-(g_*,\tfrac12) = 0\).

---

## 6. Indexed duality compatibility

\[
g_*(1-x) = 4(1-x)^3 - 6(1-x)^2 + 3(1-x) = 1 - g_*(x).
\]

Therefore \(g_1 = g_2 = g_*\) satisfies

\[
g_1(x) + g_2(1-x) = g_*(x) + g_*(1-x) = 1.
\]

**Duality auditor note:** GL24 §4.1 states \(\ell(\gamma,\theta,\alpha)+\ell(\gamma,\pi-\theta,\beta)=\mathrm{Area}(\gamma)\). Normalizing by area and \(x=\theta/\pi\), this becomes \(g_\alpha(x)+g_\beta(1-x)=1\). The cubic satisfies this with **\(g_1=g_2\)** — stronger than generic indexed duality. This is compatible with the normalization but does **not** prove realizability by distinct Floer invariants \(\ell(\cdot,\cdot,\alpha)\) and \(\ell(\cdot,\cdot,\beta)\).

---

## 7. Implementation

| Module | Role |
|--------|------|
| `cubic_countermodel.py` | Direct rational polynomial |
| `cubic_independent_verify.py` | SymPy (no import from above) |
| `tests/test_cubic_countermodel.py` | Regression |
| `tests/test_cubic_independent_verify.py` | Agreement test |

---

## Model classification

| Axiom | Satisfied |
|-------|-----------|
| Model S endpoints | Yes |
| Model S strict bijection | Yes |
| κ-Lipschitz for κ≥3 | Yes |
| Subadditivity (continuum) | Yes (algebraic) |
| Indexed duality | Yes (with g₁=g₂) |
| D⁺(g*,½)=0 | Yes |

**Does not satisfy:** spectrality, Floer grading, barcode data, derivative = squared radius of genuine rectangle, diagonal exclusion.
