# T038-Curve Clean-Room Audit

**Reviewer:** Independent reconstruction (Directive 019)  
**Verdict:** `T038_CURVE_CLEAN_ROOM_VERIFIED`

---

## Scope

Parametrized \(C^0\) theorem only:
\[
\|\gamma - \gamma_0\|_\infty < \eta
\]
under a **fixed degree-one** parametrization. Not an unparametrized Fréchet-neighborhood theorem.

---

## Audit checklist

| # | Question | Result |
|---|----------|--------|
| 1 | \(G(\tau u)=AG(u)\), \(D(\tau u)=-D(u)\) exact? | **Yes** — verified numerically + algebraically |
| 2 | Rhombus class survives \(C^0\) perturbation? | **Yes** — \(E_G(\eta)<m_G\) at \(\eta=0.01\) |
| 3 | Free cyclic action on \(U\)? | **Yes** — no \(\tau^k u=u\) for \(k=1,2,3\) |
| 4 | Sign line Möbius on quotient circle? | **Yes** — \(\chi(\tau)=-1\) |
| 5 | \(\langle w_1(L_\chi),[\overline Z]_2\rangle=1\)? | **Yes** |
| 6 | Nowhere-zero \(\overline D_\gamma\) trivializes line? | **Yes** — twisted-section zero lemma |
| 7 | Collisions excluded? | **Yes** — margin in neighborhood |
| 8 | Continuous limit preserves square? | **Yes** — smooth approximation + compactness |
| 9 | Distinct from cokernel \(DF\)? | **Yes** — Directive 017 cokernel trivial |
| 10 | Curve-induced structure only? | **Yes** — not arbitrary map perturbation |

---

## Key independent checks

- \(A^4=I\), \(\det A=-1\)
- \(\rank DG=3\), \(\ker=\mathrm{span}(1,1,1,1)\)
- \(m_G \approx 0.331\) reproduced (`rhombus_continuation.py`)
- Square recovery: \(G=0 \land D=0 \Rightarrow\) nondegenerate square on circle family

---

## Not claimed

- Fréchet-invariant formulation (optional future work)
- Sharp quantitative \(\eta_{\mathrm{circle}}\) (Lipschitz constant conservative)
- Abstract **T038′** (Euler cokernel bundle) — remains `CONJECTURAL_TARGET`

Implementation: `t038_clean_room.py`
