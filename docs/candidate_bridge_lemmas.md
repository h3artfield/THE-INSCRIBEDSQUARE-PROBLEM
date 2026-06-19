# Candidate Bridge Lemmas

Three candidates to exclude collapse profiles like g_* from **realizable** spectral invariants.

---

## Candidate A — Filtered product rigidity at half-angle

**Statement (precise).** Let \(\gamma\) be a smooth Jordan curve, \(r\in(0,1/2]\). Let \(\alpha\in\mathrm{JF}_2(\gamma,r,\pi/2)\) be the generator. If

\[
l_2(\gamma,r,\pi) = l_2(\gamma,r,\tfrac\pi2) + l_2(\gamma,r,\tfrac\pi2),
\]

then the Floer product pairing realizing subadditivity at \(\theta_1=\theta_2=\pi/2\) cannot be represented solely by cycles supported on the **diagonal** of \(\gamma\times\gamma\); at least one contributing trajectory has action \(>0\) and microsupport off \(\Delta(\gamma)\).

**Why excludes g_*:** g_* has zero derivative (formal R²) at half-angle — diagonal collapse.

**Source path:** GL24b Prop. 3.6 + Morse-Bott unit argument; strengthen with diagonal support control.

**Obstacles:** Equality may occur with mixed diagonal/off-diagonal in limit; not proved.

**Stronger than necessary?** Possibly — only need positive radius at \(\pi/2\), not full product rigidity.

---

## Candidate B — Square-angle microlocal vanishing (Asano–Ike)

**Statement (precise).** For rectifiable Jordan curve \(\gamma\) with sheaf \(F_\gamma\), the natural map

\[
H^*(\operatorname{Hom}(F_\gamma, R_{\pi/2} F_\gamma)) \to H^*(\Gamma(\{\tau>0\}; \mu hom(F_\gamma, R_{\pi/2} F_\gamma)))
\]

has kernel containing no class whose microsupport is contained in \(\Delta(\gamma)\times\{\tau=0\}\).

**Why excludes g_*:** g_* models zero-radius; AI24 nondegenerate rectangle requires off-diagonal intersection.

**Source path:** AI24 §4 sheaf condition + cofiber sequence.

**Obstacles:** Extending beyond rectifiable; connecting to Floer \(l_2\).

**Stronger than necessary?** No — close to AI24 framework.

---

## Candidate C — Positive barcode gap at θ=π/2

**Statement (precise).** For smooth approximants \(\gamma_n\to\gamma\) and spectral invariant \(l_2\), the barcode of \(\mathrm{JF}_2(\gamma_n,r,\cdot)\) contains an interval \([a,b]\) with \(b-a\ge\varepsilon>0\) crossing \(\theta=\pi/2\) whose endpoint actions correspond to nondegenerate rectangles, and this bar persists in the C⁰ limit.

**Why excludes g_*:** g_* has zero slope at \(\pi/2\) — no positive action gap.

**Source path:** GL26 Scholium 2.3 + barcode stability (not in source for Jordan Floer).

**Obstacles:** Barcode stability for non-smooth limits unproved.

**Stronger than necessary?** Yes.

---

## Ranking

| Criterion | A | B | C |
|-----------|---|---|---|
| Closeness to source | Medium | **High** | Low |
| New definitions | Medium | Low | High |
| Nonrectifiable | Partial | Partial | Unknown |
| C⁰ limits | Partial | **Good** | Hard |
| Excludes g_* | Yes | **Yes** | Yes |
| Finite toy testing | Hard | Medium | Hard |
| Foundation risk | Medium | **Low** | High |
| Likely false? | Medium | **Low** | Medium |

---

## Selected target: **Candidate B — SOURCE_REPRODUCTION / CALIBRATION**

> Reproduce AI-PEG-v3 chain: rectifiable → primitive convergence → microsupport disjointness → diagonal exclusion → off-diagonal rectangle.

**Not** the next original theorem until calibration is verified against AI-PEG-v3.

---

## Former Candidate B (microlocal lemma)

Reclassified from "next theorem target" (Directive 004) to calibration exercise (Directive 005).

---

## Ranked research target after calibration

**T017** (finite \(p\)-variation bridge) — see `docs/finite_p_variation_bridge.md`.

**First unresolved sublemma (Outcome B):**

> **Approximation Lemma (T017-A).** For Jordan \(c\) with \(|c|_{p\text{-var}}<\infty\), \(1\le p<2\), and fixed \(p<q<2\), there exist **simple** polygonal (or \(C^1\)) Jordan approximants \(c_n\) such that \(c_n\to c\) uniformly and \(\|c_n-c\|_{q\text{-var}}\to 0\).

Without T017-A, Young primitive convergence (T017-B) cannot be attempted.
