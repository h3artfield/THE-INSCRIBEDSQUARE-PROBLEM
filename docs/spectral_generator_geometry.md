# Spectral Generator Geometry

**Purpose:** Document data discarded when reducing Jordan Floer / sheaf theory to scalar \(g(x)=\ell(\pi x)/A\).

**Sources:** GL24b §2–3, GL26 §1, AI24 §1–4

---

## Jordan Floer (Greene–Lobb trapezoid/rectangle setting)

| Data | Description | Source |
|------|-------------|--------|
| Chain complex | \(\mathrm{JFC}(\gamma,r,\theta,h_t)\) | GL24b |
| Homology | \(\mathrm{JF}_i(\gamma,r,\theta)\), \(i=1,2\) | GL24b |
| Generators | Trajectories / critical points of action functional | GL24b §2 |
| Grading | Maslov index (integer) | GL24b |
| Action filtration | Real action; spectral invariant = inf action of cycle | GL24b §3 |
| Spectral invariants | \(l_1, l_2\) — one per nonzero degree | GL24b |
| Spectrality | \(l_2(\theta)\) = action of inscribed trapezoid/rectangle | GL24b |

---

## Which generators are genuine rectangles?

- **Non-constant trajectories** with action = spectral invariant (GL24b §3).
- **Diagonal / degenerate** configurations: intersection of \(C\times C\) with \(R_\theta(C\times C)\) on diagonal \(\Delta_C\) (AI24).
- Near \(\theta=\pi/2\): inscribed rectangles; limit may shrink to diagonal (shrinkout).

---

## Continuation in θ

- Spectral invariants continuous in \(\theta\) (GL24b Prop. 3.5).
- Product \(\star\) respects continuation (GL24b Prop. 3.6 proof).
- **Branch termination:** not audited — generators may persist or die; scalar \(g\) records only inf action.

---

## Sheaf side (Asano–Ike)

| Data | Description |
|------|-------------|
| Object | \(F_C \in \mathcal{T}^\eta(T^*M^2)\) — sheaf quantization of \(C\times C\) |
| Microsupport | Legendrian lift \(\Lambda\) of curve × curve |
| Hom | \(\operatorname{Hom}(F_C, R_\theta F_C)\) |
| Microlocal Hom | \(\mu hom(F_C, R_\theta F_C)\) on \(\{\tau>0\}\) |

Rectangle existence linked to **nonzero** Hom / vanishing of microlocal obstruction (AI24 §4).

---

## What scalar g(x) discards

1. Grading (\(\mathbb{F}_2\) in degree 2 vs 1)
2. Barcode / persistence across θ
3. Microsupport location (diagonal vs off-diagonal)
4. Homological representative type
5. Product structure under \(\star\)
6. Hamiltonian perturbation data \((h_t, J_t)\)
7. Multiple branches with same action
8. Orientation / sign data

---

## g_* vs genuine spectral profile

g_* is a **scalar** satisfying Level F. It **cannot** encode:

- whether achieving generators lie on diagonal;
- whether a bar persists through \(\theta=\pi/2\);
- whether \(\mu hom=0\) at square angle.

**Next target:** bridge lemma forcing off-diagonal generator or positive microlocal gap at \(\theta=\pi/2\).
