# T020 — Critical-Modulus Rectangular Peg Theorem

**Status:** CONJECTURAL_TARGET (Directive 008 Outcome B)

---

## Statement

Let \(c:S^1\to\mathbb R^2\) admit parametrization with modulus \(M<\infty\), nondecreasing \(m\) with \(m(r)\to 0\), \(\int_0^1 m(r)^2/r\,dr<\infty\), and

\[
\|c(t)-c(s)\|\le M\,d_{S^1}(s,t)^{1/2}\,m(d_{S^1}(s,t))
\]

for small circle distance. Then \(c\) satisfies AI-PEG-v3 Theorem 1.1.

**Parametrization dependence:** Stated for a **chosen** parametrization satisfying the modulus — not purely a property of the trace.

---

## Proved sublemma (§8)

\[
\sum_i|c(t_{i+1})-c(t_i)|^2 \le M^2 m(\delta)^2
\]

on partitions of mesh \(\le\delta\) (one period). Hence \(\omega_2(c,\delta)\le Mm(\delta)\to 0\).

Periodic seam: choose basepoint on unchanged edge (T018 §9 convention).

---

## Yang enhancement (imported)

Yang Thm 33: such \(\gamma\in\mathcal G_2\).

---

## Blocking step (Outcome B)

**BG simple Jordan interpolants \(P_n\):** Yang Thm 23 applies to **area of PL approximants of the same path** on refining partitions. BG Thm 2.2 selects partitions for **simplicity**, not arbitrary refinement.

**Verdict:** **UNRESOLVED** whether BG partition sequence yields the same 1-variation area convergence as Yang's generic PL family.

See `docs/simple_polygon_rough_convergence.md`.

---

## Verdict

**Outcome B — Polygonal enhancement mismatch**
