# Directive 018 Report

**Date:** 2026-06-18  
**Outcome:** **A — T038-Curve proved (PROVED_LOCALLY)**

---

## Verdicts

| Item | Status |
|------|--------|
| Rhombus/diagonal split | Verified exact |
| Cyclic equivariance \(G(\tau u)=AG(u)\), \(D(\tau u)=-D(u)\) | Verified |
| Circle \(\rank DG=3\), expected \(DF\) | Verified |
| First-order \(\delta D_h\) anti-periodic | Verified (calibration) |
| Rhombus boundary margin \(m_G\) | ~0.33 |
| Sign line \(L_\chi\) | Möbius, \(w_1=1\) |
| Cokernel line (Dir. 017) | Trivial — **distinct** |
| T038-Curve | **PROVED_LOCALLY** |
| T039 | CONJECTURAL_GENERALIZATION |
| T038′ | CONJECTURAL_TARGET (not closed) |
| T032§ | CONJECTURAL_FULL_BRIDGE (not attacked) |
| T036-N | Not attempted |

---

## Proof summary

1. \(F=(G,D)\); \(G^{-1}(0)\) is \(\tau\)-invariant for every curve.
2. Rhombus continuation \(R_\gamma\) persists when \(E_G(\eta)<m_G\).
3. \(D\) descends to \(\overline D_\gamma\) section of Möbius bundle \(L_\chi\) over \(\overline R_\gamma\).
4. \(\langle w_1(L_\chi),[\overline Z]_2\rangle=1\); nowhere-zero \(\overline D_\gamma\) impossible.
5. \(\exists u\in R_\gamma\) with \(D_\gamma(u)=0\) ⇒ square; continuous limit via smooth approximation.

---

## Clean-room audit (10 questions)

| # | Answer |
|---|--------|
| 1 | Yes — exact matrix \(A\), verified numerically |
| 2 | Yes — for \(\eta=0.01\), \(E_G<m_G\) |
| 3 | Yes — free on ordered collision-free \(U\) |
| 4 | Yes — \(L_\chi|_{\overline Z}\) Möbius |
| 5 | Yes — pairing \(=1\) |
| 6 | Yes — trivial section contradicts \(w_1\) |
| 7 | Yes — margins in neighborhood definition |
| 8 | Yes — uniform limit lemma stated |
| 9 | Yes — bundles explicitly distinct |
| 10 | Yes — curve perturbations only |

---

## Rank-5 families

No automatic CYCLIC_ODD_CERTIFIED from circle proof. Status: **UNPROTECTED_FAMILY** unless separately audited.

---

## Git

**Tag:** `directive-018-cyclic-odd-rhombus-internal-2026-06-18`

**Tests:** 19+ new in `tests/test_cyclic_odd.py`

---

## External consistency

Known quantitative near-circle results used as benchmark only, not as proof gap-fill.
