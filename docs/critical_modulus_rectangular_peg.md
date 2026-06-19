# T020 — Critical-Modulus Rectangular Peg Theorem

**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 008R Outcome A)

**Historical:** Directive 008 Outcome B superseded — see F011 closure in `docs/solver_failure_history.md`.

---

## Statement

Let \(c:S^1\to\mathbb R^2\) admit an orientation-preserving parametrization on \([0,1]\) with modulus \(M<\infty\), nondecreasing \(m\) with \(m(r)\to 0\), \(\int_0^1 m(r)^2/r\,dr<\infty\), and

\[
\|c(t)-c(s)\|\le M|t-s|^{1/2}m(|t-s|)
\]

for small \(|t-s|\) (circle distance after lifting to \([0,1]\) with seam convention as in T018).

Then \(c\) satisfies Asano–Ike Theorem 1.1 and inscribes every \(\theta\)-rectangle for \(\theta\in(0,\pi)\).

**Parametrization dependence:** Stated for a parametrization satisfying the modulus.

---

## Proof chain (008R)

1. **Vanishing 2-var** from modulus (sublemma).
2. **Yang Thm 33:** \(\|A(c^{D_1})-A(c^{D_2})\|_{1-var}\to 0\) for all fine partitions — Cauchy family.
3. **Yang Thm 23:** limit area \(\mathbb A_c\); \(c\in G_2(\mathbb R^2)\).
4. **BG Thm 2.2:** simple Jordan \(P_n=c^{D_n}\), \(\|P_n-c\|_\infty\to 0\) (Lemma 3.1 for uniform).
5. **Area \(\Rightarrow\) primitive:** `docs/critical_area_to_liouville_primitive.md`.
6. **T018 (frozen):** \(C^1\) \(S_n\), adaptive \(\varepsilon_n\) — `docs/critical_smoothing_primitive_control.md`.
7. **Period lift + AI-PEG-v3 Thm 1.1.**

---

## Audit

`docs/t020_clean_room_audit.md`

---

## Verdict

**Outcome A — Critical bridge proved**
