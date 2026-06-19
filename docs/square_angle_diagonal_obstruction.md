# Square-Angle Diagonal Obstruction (Asano–Ike)

**Source:** Asano–Ike, arXiv:2412.21057v3

**Notation:** As in AI24; \(\theta=\pi/2\) specialization.

---

## 1. Object assigned to Jordan curve C

Sheaf quantization \(F_C \in \mathcal{T}^\eta(T^*M^2)\) with microsupport on Legendrian lift of \(C\times C\) (AI24 §1–3).

---

## 2. Continuous Legendrian lift hypothesis

For rectifiable / locally monotone curves, \(F_C\) exists via interleaving limit (AI24 Thm 1.1). Legendrian lift \(\Lambda\) of \(C\times C\) in contact \(T^*M^2\times\mathbb{R}_t/\pi\mathbb{Z}\).

---

## 3. Diagonal / microlocal Hom term

Cofiber sequence (AI24 §2, Lem. 2.x):

\[
\operatorname{colim}_{\varepsilon\to0} \operatorname{Hom}(F_C, T_{-\varepsilon} R_\theta F_C) \to \operatorname{Hom}(F_C, R_\theta F_C) \to \Gamma(\{\tau>0\}; \mu hom(F_C, R_\theta F_C)).
\]

**Microlocal term** \(\mu hom\) captures obstruction supported at \(\{\tau>0\}\) (Reeb / time direction).

---

## 4. Required vanishing

Existence of **nondegenerate** \(\theta\)-rectangle (off diagonal) is related to **nonzero** \(\operatorname{Hom}(F_C, R_\theta F_C)\) or equivalently conditions ensuring microlocal obstruction does not block (AI24 §4 — sheaf-theoretic condition for rectangle).

At diagonal: \(R_\theta(z,z)=(z,z)\) always — degenerate.

---

## 5. Implication

If sheaf-theoretic condition holds (e.g. AI24 Thm 1.1 hypotheses: rectifiable or locally monotone), then \(\theta\)-rectangle exists for all \(\theta\in(0,\pi)\).

**Specialize \(\theta=\pi/2\):** inscribed **square-angle rectangle** (diagonal angle \(\pi/2\)).

---

## 6. Curve classes covered

| Class | Result |
|-------|--------|
| Rectifiable | AI24 Cor. 1.2 |
| Locally monotone | AI24 Cor. 1.3 |
| Smooth | GL21 / AI24 |
| Zero-measure nonrectifiable | **NOT COVERED** |

---

## 7. Conditional theorem (square peg)

> **Conditional (AI24 + specialization).** If for every Jordan curve \(\gamma\) and \(\theta=\pi/2\), the microlocal obstruction \(\Gamma(\{\tau>0\};\mu hom(F_\gamma, R_{\pi/2} F_\gamma))\) vanishes in the sense required by AI24 §4, then every rectifiable / locally monotone Jordan curve inscribes a square-angle rectangle. Combined with AI24 coverage and known reductions, this yields squares for all curves in the **already-solved** classes.

**Dependency chain:** AI24 Thm 1.1 → all \(\theta\) rectangles → \(\theta=\pi/2\) square-angle rectangles → squares for rectifiable/locally monotone.

**Gap for universal conjecture:** curves outside AI24 class; reduction from square peg to AI24 diagonal vanishing for **all** Jordan curves — **open**.

---

## Relation to g_*

g_* has **zero formal radius** at \(x=\tfrac12\). AI24 obstruction is **cohomological**, not scalar. g_* does not prove or disprove AI24 diagonal vanishing for any curve.

---

## Residual obstruction for universal square peg

For a **general** Jordan curve not covered by AI24:

1. Sheaf quantization may exist (continuous limit).
2. Microlocal Hom at \(\theta=\pi/2\) may not vanish.
3. Scalar Level-F profile could resemble g_* while Hom data differs.

**First sublemma:** Compare AI24 §4 condition at \(\theta=\pi/2\) with Floer derivative property (GL26 Thm 5.1) on a common rectifiable class.
