# Directive 004 Report — Strict Countermodel Closure

**Date:** 2026-06-18  
**Status:** Complete  
**Verdict:** Level-F Model S insufficiency for κ≥3; pivot to Candidate B (AI24 diagonal obstruction)

---

## Part I — Cubic countermodel verification

| # | Question | Answer |
|---|----------|--------|
| 1 | All Level-F Model S axioms? | **Yes** (κ≥3) |
| 2 | Lip constant 3? | **Yes** |
| 3 | Continuum subadditivity? | **Yes** — \(H=12xy(1-x-y)\) |
| 4 | Indexed duality? | **Yes** — \(g_*(1-x)=1-g_*(x)\) |
| 5 | \(D^+(g_*,\tfrac12)=0\)? | **Yes** — \(D_h=4h^2\) |
| 6 | Outcome B superseded? | **Yes** for Model S, κ≥3 (T015) |

Dual verification: SymPy + rational (`cubic_independent_verify.py` / `cubic_countermodel.py`) — **agree**.

---

## Part II — What g_* evades

Scalar Level F only. **Absent:** spectrality, Floer grading, barcodes, microlocal Hom, off-diagonal generator persistence, positive \(R^2\) at \(\pi/2\).

Formal collapse signature: \(g_*'( \tfrac12)=0 = R^2\) if derivative interpreted as squared radius.

See `docs/cubic_countermodel_property_matrix.md`.

---

## Part III — Source audits

| Doc | Key finding |
|-----|-------------|
| `square_angle_operator_audit.md` | \(R_{\pi/2}^2=R_\pi\) on \(\mathbb{C}^2\) (AI24); **no** Floer Z₄ |
| `half_angle_equality_audit.md` | Equality at \((\tfrac12,\tfrac12)\) automatic for g_*; **no** rigidity theorem |
| `spectral_generator_geometry.md` | Scalar g discards grading, Hom, μhom |
| `square_angle_diagonal_obstruction.md` | AI24 conditional at \(\theta=\pi/2\) |

---

## Part IV — Bridge lemma selection

**Selected: Candidate B** — AI24 half-angle microlocal / diagonal obstruction.

**First sublemma (B.1):** For rectifiable \(\gamma\), relate \(\mu hom(F_\gamma,R_{\pi/2}F_\gamma)\) support to existence of off-diagonal representative with action \(l_2(\gamma,r,\pi/2)\).

See `docs/candidate_bridge_lemmas.md`.

---

## Part V — Synthetic spectrum

Single branch with \(a'(x)=g_*'(x)\) **can** represent g_* (diagnostic). **Reflection symmetry holds** at both action and derivative levels: \(g_*(1-x)=1-g_*(x)\) and \(g_*'(1-x)=g_*(x)\). Neither excludes the cubic profile (F007).

---

## Ledger

- **T015** added — strict smooth Model S countermodel, κ≥3
- **T014W** retained (historical Model W)
- **Directive 003R Outcome B** superseded for Model S

---

## Report answers (§13)

1. Yes (κ≥3)  
2. Yes, Lip=3  
3. Yes, algebraic  
4. Yes  
5. Yes, D⁺=0  
6. Yes, superseded by T015  
7. Grading, Hom, μhom, barcodes, spectrality  
8. \(R_{\pi/2}^4=I\) on config space only; **no** established Floer Z₄  
9. Equality not rigid at scalar level; potentially rigid under filtered product (unproved)  
10. AI24 μhom / Hom cofiber obstruction at \(\theta=\pi/2\)  
11. **Candidate B**  
12. **Sublemma B.1** (see candidate_bridge_lemmas.md)

---

## Acceptance checklist

- [x] Cubic identities verified exactly (dual implementation)
- [x] Strict monotonicity proved conventionally
- [x] Subadditivity factorization verified
- [x] Model S Level-F insufficiency updated (κ≥3)
- [x] Scalar vs spectral separated
- [x] Square-angle operators source-audited
- [x] AI24 diagonal obstruction stated
- [x] No invented Z₄
- [x] Synthetic tests labeled diagnostic
- [x] One bridge lemma selected
- [x] First sublemma precise
