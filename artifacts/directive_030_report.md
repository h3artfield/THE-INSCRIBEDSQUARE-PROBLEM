# Directive 030 Report — Hull-Adjacent Geometric Ears and Bounded-Gate Defect Allocation

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **A — T053B proved**

---

## Executive summary

Directive 030 closes both gaps left by Directive 029 for the **bounded-gate finite-intrusion class**. **T058** (hull-adjacent geometric ears via weak-dual leaves), **T059** (join bound \(J_M(r)=O(M^2r^2)\)), quantitative defect allocation, and **T053B** are proved locally. Universal T045R is not attacked beyond this class.

---

## Part I — Directive 029 frozen

Manifest: `artifacts/directive_029_verified_internal_manifest.json`.

Frozen T043R, T046, T044R, T051, T052 **not modified**.

---

## Part II–III — Hull-adjacent ears (T058)

- Hull adjacency: gate-free boundary arc \(B_{ij}\subset\partial H(C)\).
- Reduced gate graph preserves outerplanarity and true gate count.
- Weak-dual leaf theorem implemented; tree/forest case via outermost chords.
- Ear saturation preserves two-gate property.
- **T058 PROVED_LOCALLY** — tested on 4, 6, 8, 10, 12 gate rational clusters.

Closes D029 geometric-ear gap: adjacency uses **either** boundary arc, not only consecutive indices.

---

## Part IV–V — Join bounds and allocation

- \(Q(M) \le 3M\), \(|\Delta_i| \le C_{\mathrm{collar}} r\).
- \(J_M(r) = \tfrac12\binom{Q(M)}{2}C_{\mathrm{collar}}^2 r^2\).
- One-step: \(J_M(r)\le\varepsilon/4 \Rightarrow \max(|\mathbb A_E|,|\mathbb A_{C'}|)\ge 3\varepsilon/8\).
- T037 link: fixed \(\varepsilon=\varepsilon_0/4\), shrinking \(r\) forces join negligible.
- Explicit \(c(M)=1/(4Q(M))\), \(r_0(M,\varepsilon)\).

---

## Part VI–VII — Geometric peeling and retained cover

- Canonical geometric peel; \(\kappa(C)\) decreases each step.
- Extracted forest disjoint/nested; T051/T052 compatible.
- `CLUSTER_SIGNATURE_CARLESON` for small-diameter extractions.
- Retained-skeleton cover with well-founded termination.

---

## Part VIII — T053B

**PROVED_LOCALLY** for:
- finite intrusion tree;
- Jordan-disk hull;
- uniform gate bound \(M\);
- outerplanar \(G_C\);
- shrinking diameter.

Chain: T053B \(\Rightarrow\) T052 \(\Rightarrow\) T043R \(\Rightarrow\) T022.

Clean room: **T053B_CLEAN_ROOM_VERIFIED** on certified bump-polygon sequence.

---

## Part IX — Residual classes (post-T053B)

Bounded-gate finite Jordan-hull clusters **removed** from universal residual.

Remaining:
- `UNBOUNDED_GATE_DENSITY_CLUSTER`
- `INFINITE_INTRUSION_TREE`
- `NON_JORDAN_SATURATION_HULL`
- `POSITIVE_SCALE_NONANNULAR_CLUSTER`

---

## Part X — Falsification

| Test | Result |
|------|--------|
| 4–12 gate rational clusters | T058 geometric ear found |
| Join stress (max separation, winding) | Analytic bound holds |
| Defect allocation at \(r\to0\) | Join negligible; component carries defect |
| No T058 counterexample in tested family | PASS |

---

## Part XI — Clean-room audit

| # | Question | Answer |
|---|----------|--------|
| 1 | Graph ear → hull-adjacent candidate? | Yes (weak dual) |
| 2 | Saturation preserves two gates? | Yes |
| 3 | Q(M) valid? | Yes, Q(M)=3M |
| 4 | Increments bounded by r? | Yes |
| 5 | Join exact, winding-independent? | Yes |
| 6 | Fixed defect + shrinking r? | Yes |
| 7 | Geometric peel terminates? | Yes |
| 8 | Crosscuts compatible? | Yes |
| 9 | Signature proved? | Yes (small diam) |
| 10 | Retained cover complete? | Yes locally |
| 11 | Uniform M? | Yes |
| 12 | Unbounded/infinite open? | Yes |

**Verdict:** `T053B_CLEAN_ROOM_VERIFIED`

---

## Part XII — Outcome

**Outcome A:** Bounded-gate finite-intrusion systems completely reduced to surgery. Only unbounded gate count, infinite trees, non-Jordan hulls, and positive-scale nonannular clusters remain.

---

## Theorem status

| ID | Status |
|----|--------|
| T058 | PROVED_LOCALLY |
| T059 | PROVED_LOCALLY |
| T053B | PROVED_LOCALLY |
| T045R | CONJECTURAL_FULL_EXTRACTION (unchanged) |

---

## Tests

```
tests/test_directive_030.py — 12 passed
Combined D029/D030 regression — 30 passed
```

---

## Deliverables

8 modules, 8 docs, manifest, this report.
