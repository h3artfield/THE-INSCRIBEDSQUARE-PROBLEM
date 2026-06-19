# Simple Polygon Rough Convergence (BG vs Yang)

**Directive 008 §12 answer (historical):** UNRESOLVED  
**Directive 008R answer:** **YES** — BG polygons are Yang interpolants; universal area convergence applies.

---

## Resolution (008R)

Yang Theorem 33 proves \(\{A(c^D):|D|\le\delta\}\) is Cauchy in 1-variation for **all** partitions (not one sequence). Theorem 23 quantifier: **`ALL_PARTITIONS`**.

In \(\mathbb R^2\), BG minimizing geodesics are straight chords = Yang eq. (4). Hence \(P_n=c^{D_n}\) as parametrized maps.

See `docs/bg_equals_yang_interpolant.md`, `docs/yang_theorem23_quantifier_audit.md`.

---

## Historical gap (Directive 008 — superseded)

The 008 concern that "simplicity constraint" might select a non-cofinal partition family is **not** load-bearing once Thm 33's all-partition Cauchy estimate is applied: **any** mesh \(\to 0\) family, including BG's, converges to the same \(\mathbb A_c\).

---

## Verdict

Polygonal enhancement mismatch **closed**. T020 Outcome A.
