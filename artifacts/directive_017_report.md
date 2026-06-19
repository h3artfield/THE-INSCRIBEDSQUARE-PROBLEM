# Directive 017 Report

**Date:** 2026-06-18  
**Outcome:** **B — Abstract T038′ framework; circle requires curve-restricted structure**

---

## Main verdict

| Item | Result |
|------|--------|
| Countermodel | Normal nondegeneracy **insufficient** |
| Cokernel bundle | Defined; Lyapunov–Schmidt section formalized |
| Euler obstruction | \(\langle w_d(E),[Z]_2\rangle\ne0\) is the correct target invariant |
| Circle monodromy | `CIRCLE_OBSTRUCTION_LINE_TRIVIAL` |
| Circle family | **Circle-B** — trivial obstruction on ordered and cyclic quotient |
| T038′ | CONJECTURAL_TARGET (statement + proof route) |
| T038-Curve | CONJECTURAL (formulated, not proved) |
| \(\rho_\square^{\mathrm{gen}}\) | **Invalid** as persistence invariant without obstruction |
| \(\rho_\square^{\mathrm{obs}}\) | Replaces gen; rank-5 families rejected |
| T032‡ | CONJECTURAL_FULL_BRIDGE (primary bridge) |
| T036-N | **Not attempted** |

---

## Circle obstruction computation

Ordered family \(z(t)=(t,t+\pi/2,t+\pi,t+3\pi/2)\):

- \(\rank DF = 3\), \(\ker DF=\mathrm{span}(1,1,1,1)\)
- Cokernel line: trivial bundle (\(w_1(E)=0\), monodromy +1)
- Cyclic quotient (\(\pi/2\)): also trivial

Local normal index = 1 does **not** imply protection.

---

## Why Outcome B (not A or C alone)

- **Not A:** \(\langle w_1(E),[S^1]_2\rangle=0\) on circle
- **Not D (quotient):** quotient obstruction also trivial
- **Not E:** Lyapunov–Schmidt framework is valid; gap is Euler class on circle, not foundational
- **B:** Abstract T038′ is the correct theorem target; circle needs **T038-Curve** for curve-induced perturbations

---

## Code

New modules under `src/squarepeg/robust_degree/`:

- `morse_bott_countermodel.py`
- `cokernel_bundle.py`
- `obstruction_section.py`
- `euler_class.py`
- `circle_cokernel.py`
- `circle_quotient.py`
- `curve_induced_section.py`
- `valid_family_certificate.py`
- `obstruction_radius.py`

Tests: `tests/test_obstruction_bundle.py`

---

## Status language (frozen)

| ID | Status |
|----|--------|
| T037 | PROVED_LOCALLY |
| T038 | CONJECTURAL |
| T038′ | CONJECTURAL_TARGET |
| T038-Curve | CONJECTURAL |
| T032‡ | CONJECTURAL_FULL_BRIDGE |
| T032† | Superseded as primary |
| T036-N | CONTROLLED_CLASS_TARGET |

**Tag:** `directive-017-obstruction-bundle-audit-internal-2026-06-18`
