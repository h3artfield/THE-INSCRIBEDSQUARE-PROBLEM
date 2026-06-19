# Square-Angle Operator Audit

**Sources:** GL24 (2404.05179), AI24 v3 (2412.21057), GL26 (2604.17116v1)

**Rule:** No Z₄ action is treated as established unless sourced.

---

## Rectangle rotation operator (AI24 §1, GL24)

**Space:** \(R_\theta : \mathbb{C}^2 \to \mathbb{C}^2\) acts on configuration space of ordered pairs \((z,w)\).

**Definition (AI24):** For \(\theta \in [0,\pi]\),

\[
R_\theta(z,w) = (e^{i\theta} z, w).
\]

(Exact formula in source; planar rotation of first factor.)

**At \(\theta = \pi/2\):**

\[
R_{\pi/2}(z,w) = (i z, w).
\]

**Diagonal:** \(R_\theta(z,z)=(z,z)\) for all \(\theta\) (AI24). Degenerate rectangles lie on \(\Delta_C\).

---

## Does \(R_{\pi/2}^2 = R_\pi\)?

On \((z,w)\):

\[
R_{\pi/2}^2(z,w) = R_{\pi/2}(iz,w) = (i^2 z, w) = (-z, w).
\]

\[
R_\pi(z,w) = (-z, w).
\]

**Verdict:** \(R_{\pi/2}^2 = R_\pi\) as literal maps on \(\mathbb{C}^2\). **SOURCE:** direct computation from AI24 definition.

---

## Does \(R_{\pi/2}^4 = I\)?

\[
R_{\pi/2}^4(z,w) = (z,w).
\]

**Verdict:** Yes on \(\mathbb{C}^2\). This is **planar rotation on one factor**, not a genuine \(\mathbb{Z}_4\)-symmetry of the **inscribed square problem** on Jordan curves.

---

## Lift to categories

| Theory | Lift | Reference |
|--------|------|-----------|
| Tamarkin / sheaves (AI24) | \(R_\theta\) lifts to \(\mathcal{T}^\eta\); action on \(F_C\) | AI24 §1, GKS |
| Jordan Floer (GL24b) | Hamiltonian \(G_{r,\theta}\) on \(\gamma\times\gamma\) | GL24b §2 |

**Grading / action shifts:** AI24 lift may involve degree shifts in \(\mathcal{T}^\eta\); not fully audited here. **CONJECTURAL:** no clean \(\mathbb{Z}_4\)-graded Floer group at \(\theta=\pi/2\) is stated in sources.

---

## Square angle vs trapezoid angle

GL26 / GL24b use **isosceles trapezoid** spectral invariants \(l_2(\gamma,r,\theta)\), not rectangle invariants, for the square route. Rectangle theory (AI24, GL24) uses **two angles** \(\theta\) and \(\pi-\theta\) with **indexed duality** \(\ell(\gamma,\theta,\alpha)+\ell(\gamma,\pi-\theta,\beta)=\mathrm{Area}\).

**Do not conflate** trapezoid Floer at aspect ratio \(r\) with rectangle Floer at \(\theta=\pi/2\).

---

## Z₄ action

| Claim | Status |
|-------|--------|
| \(R_{\pi/2}^4 = I\) on \(\mathbb{C}^2\) | SOURCE (AI24 definition) |
| \(\mathbb{Z}_4\)-equivariant Jordan Floer homology at square angle | **CONJECTURAL / NOT IN SOURCE** |
| Order-4 symmetry of inscribed squares on a curve | **GEOMETRIC** (square symmetry), not an operator on Floer groups |

---

## Effects on spectral classes

GL24b: \(\mathrm{JF}_*(\gamma,r,\theta) \cong \mathbb{F}_2^2\) in degrees 1 and 2. Two spectral invariants \(l_1, l_2\).

At \(\theta=\pi/2\): specialization of rectangle/trapezoid framework — **no separate square-angle theorem** in sources beyond general \(\theta\)-existence (AI24 for rectifiable rectangles).

---

## Summary for Directive 004

- \(R_{\pi/2}^2 = R_\pi\) **literally** on configuration space (AI24).
- No established **Floer-theoretic** \(\mathbb{Z}_4\) action forcing square nondegeneracy.
- Square-angle research must use **diagonal exclusion** and **spectral generator** data, not planar \(R_{\pi/2}^4=I\) alone.
