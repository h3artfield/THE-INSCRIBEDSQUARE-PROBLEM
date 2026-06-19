# T034 — Protected-Box Semidecidability for Rational Polygons

**Status:** `PROVED_LOCALLY`

---

## Statement

If rational polygon \(P\) has intrinsic \(\rho_\square(P,B)>\eta>0\) on some protected box \(B\), then for every \(0<\eta'<\eta\) there exists \(k\) such that exhaustive level-\(k\) search certifies \(\underline\rho_k(P)>\eta'\).

---

## Proof ingredients

1. Square map on edge-product cell is polynomial (degree 4) with rational coefficients.
2. Protected-box conditions are open on compact rational subboxes.
3. Nonsingular degree and positive margins are stable under small rational perturbations of \(B\).
4. Rationals are dense; exhaustive search at increasing \(k\) eventually finds a certifying subbox.

---

## Consequence (T034-C)

For rational polygons:

\[
\underline\rho_\infty(P)=\rho_\square(P).
\]

Implementation: `semialgebraic_degree.py`, `exhaustive_polygon_search.py`.

Search returns `NOT_FOUND_AT_LEVEL_K` — never intrinsic zero.
