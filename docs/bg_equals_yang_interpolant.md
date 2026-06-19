# Boedihardjo–Geng Polygons Equal Yang Interpolants

**Sources:** BG-INTERPOLATION-v2 Thm 2.2; YANG-AREA-v1 Notation 9  
**Status:** PROVED (Directive 008R)

---

## BG construction (Theorem 2.2, \(M=\mathbb R^2\))

For Jordan \(\gamma:[0,1]\to\mathbb R^2\) and partition \(\mathcal P=\{t_{n,0},\ldots,t_{n,N_n}\}\), the **minimizing geodesic** interpolant \(\gamma^{\mathcal P}\) connects \(\gamma(t_{n,i})\) to \(\gamma(t_{n,i+1})\) by the shortest path in \(\mathbb R^2\).

**In \(\mathbb R^2\):** geodesics are straight line segments.

---

## Equality with Yang \(\gamma^D\)

Yang's \(\gamma^D\) (eq. (4)) is **affine in the parameter** on each \([t_j,t_{j+1}]\):

\[
\gamma^D(t)=\frac{t-t_j}{t_{j+1}-t_j}\gamma(t_{j+1})+\frac{t_{j+1}-t}{t_{j+1}-t_j}\gamma(t_j).
\]

This is exactly the chord from \(\gamma(t_j)\) to \(\gamma(t_{j+1})\) with **constant-speed parametrization in the original time variable** \(t\).

BG's minimizing geodesic segment between the same endpoints, parametrized on \([t_j,t_{j+1}]\) by the **same** \(t\), is the same map.

**Conclusion (parametrized equality):**

\[
P_n = \gamma^{D_n} = c^{D_n}
\]

as maps \([0,1]\to\mathbb R^2\), not merely as sets of vertices.

---

## Checklist

| Item | Status |
|------|--------|
| Same parameter interval \([0,1]\) | Yes |
| Affine on each subinterval | Yes (Yang (4)) |
| Vertices at partition points | Yes |
| Cyclic / closed curve | BG Jordan + periodic identification on \(S^1\) |
| Mesh \(|D_n|\to 0\) | BG: mesh \(<\varepsilon_n\), \(\varepsilon_n\to 0\) |
| Simplicity | BG Thm 2.2 guarantees simple polygon for chosen partition |

---

## Reparametrization remark

If BG used arc-length speed on each edge, an **orientation-preserving piecewise-linear reparametrization** of \([0,1]\) would relate it to Yang's \(t\)-affine form; area and Liouville primitives transform by the standard 1-variation convergence along common refinements (Yang Thm 23). **BG source uses the fixed domain partition** compatible with Yang's \(\gamma^D\).

---

## Consequence

Boedihardjo–Geng simple Jordan polygons are **not** a separate approximation scheme for area: they are Yang PL interpolants for cofinal partitions. Universal area convergence (Thm 33 + Thm 23) applies directly.
