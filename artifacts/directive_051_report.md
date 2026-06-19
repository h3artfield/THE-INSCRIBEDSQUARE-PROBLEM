# Directive 051 Report — Bellman Potentials and Critical Invariant Models

**Date:** 2026-06-19  
**Status:** Complete  
**Outcome:** **E — Diagnostic state reduction only**

---

## Executive summary

Directive 051 replaces the failed pointwise equality-core strategy (D050) with state-augmented Bellman/Lyapunov contraction. Augmented coordinates \((\Phi,R,S,J,C,B,G)\) carry retained-skeleton and sign-grouping terms explicitly. On tested models the repair stops at **compact neutral transition family** (T097): positive-scale routing prevents a certified core family, and no interval-verified Bellman contraction (T098) is established for the neutral residual.

---

## Part I — Directive 050 frozen

Manifest: `artifacts/directive_050_verified_internal_manifest.json`  
Commit: `6dc7c41`  
Tag: `directive-050-equality-core-pruning-diagnostic-internal-2026-06-19`

Exact blocker: `NORMALIZED_DEFICITS_REMAIN_ORDER_ONE`. Pointwise equality-core pruning is not coercive under current normalization.

---

## Parts II–III — Augmented state and transfer

- Seven geometric coordinates derived from attachment identity
- State cone closed and bounded on tested neutral windows
- Parent-child transfer recursion with explicit \(E(v)\) local excess
- Admissible family \(\mathscr A\) not compact on tested fixture (positive-scale routing)

---

## Parts IV–V — Bellman potentials

| Audit | Result |
|-------|--------|
| Linear search | candidates tested; no `INTERVAL_VERIFIED` contraction |
| Piecewise-linear | fallback catalogued |
| Rational certificates | `UNVERIFIED` or `RATIONAL_CANDIDATE` only |
| T098 | `CONJECTURAL_CORE_TARGET` |

---

## Parts VI–IX — Occupation measures and critical models

- Signature-weighted occupation measure defined
- Master Bellman slack \(\mathcal S_{\mathcal B}\) audited
- Coboundary correction \(\widetilde\Phi\) positive on tested nodes
- T099 not closed on neutral invariant measures

---

## Theorem status

| Theorem | Status |
|---------|--------|
| T097 | CONJECTURAL_STATE_TARGET |
| T098 | CONJECTURAL_CORE_TARGET |
| T099 | CONJECTURAL_RIGIDITY_TARGET |
| T089R | CONJECTURAL_CORE_TARGET |
| T045R | CONJECTURAL_FULL_EXTRACTION |

Clean room: **T098_REPAIRABLE_GAP**

**First exact failure:** compact admissible neutral transition family (T097) on tested models with positive-scale mass.

---

## Tests

18 passed (D051) + 148 regression = **166 passed** (D051–D042 fast suite).

---

## Next frontier

Prove T097 compactness on the pure neutral corona after excluding routed branches, or construct an exact Jordan-realizable zero-slack invariant state model (Outcome D). Close Bellman coercivity with exact arithmetic certificate or coboundary-corrected potential.

**Module count:** 12 new files under `defect_extraction/`
