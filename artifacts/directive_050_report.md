# Directive 050 Report — Deficit Budgets, Equality-Core Extraction, and T094-A Repair

**Date:** 2026-06-19  
**Status:** Complete  
**Outcome:** **E — Diagnostic deficit reduction only**

---

## Executive summary

Directive 050 repairs the T094-A compactness gap identified by Directive 049 without requiring uniform ledger equality on an entire neutral corona. The revised chain is: cumulative deficit budget → signature-weighted pruning → positive-signature equality core → uniform core deficits → simultaneous equality tangent.

On tested models the repair stops at **signature-weighted pruning**: normalized ledger deficits remain \(O(1)\) at parent signature scale, so no positive-signature good core exists as \(\epsilon\downarrow0\). A secondary blocker is semicontinuity: `RETAINED_SKELETON` and `SIGN_GROUPING` are `NOT_CLOSED` under core convergence. T093 coverage and the equality strategy are unaffected.

---

## Part I — Directive 049 frozen

Manifest: `artifacts/directive_049_verified_internal_manifest.json`  
Commit: `a90f8ea`  
Tag: `directive-049-neutral-tangent-deficit-diagnostic-internal-2026-06-19`

| Theorem | Status |
|---------|--------|
| T093 | PROVED_LOCALLY (frozen) |
| T094-A | REPAIRABLE_GAP |
| T094 | CONJECTURAL_RIGIDITY_TARGET |
| T089R | CONJECTURAL_CORE_TARGET |
| T045R | CONJECTURAL_FULL_EXTRACTION |

Exact D049 statement: `NEUTRAL_DEFICITS_NOT_UNIFORMLY_VANISHING`. Clean room: `T094_REPAIRABLE_GAP`.

---

## Parts II–III — Ledger deficits and telescoping

- Twelve raw deficits \(\delta_k\) and normalized \(d_k=\delta_k/\Phi\) implemented in `ledger_deficits.py`
- Total deficit \(\Delta(v)=\sum c_k\delta_k\) with fixed T093-derived coefficients
- Corona cumulative deficit \(\mathfrak D_L\) with explicit boundary (`0.05\Phi`) and bad-exit (`0.02\Phi`) terms
- Telescoping budget holds on tested models when \(\mathfrak D_L=o(\Phi(v))\)

---

## Parts IV–V — Distribution and pruning

| Classification | Result on binary model |
|----------------|------------------------|
| Dominant deficit class | DIFFUSE_SMALL |
| Good signature mass at \(\epsilon=0.1\) | 0 |
| T096 positive-signature core | not found |
| Markov pruning | structurally valid, signature-weighted |

---

## Part VI — T095 and T096

| Theorem | Status |
|---------|--------|
| T095 | CONJECTURAL_DEFICIT_TARGET — contraction trigger not fired (\(\eta=0\)) |
| T096 | CONJECTURAL_SELECTION_TARGET — no coherent core at fixed \(\epsilon\) |

---

## Parts VII–VIII — Compactness and semicontinuity

- Equality-core compactness framework implemented; no coherent core to normalize on tested models
- Semicontinuity audit: 10/12 deficits closed; **RETAINED_SKELETON** and **SIGN_GROUPING** = `NOT_CLOSED`
- `T094_A_UNIFORM` blocked; `T094_A_ALMOST_EVERYWHERE` not established

---

## Part IX — T094-A repair status

`CONJECTURAL_REPAIRED_TARGET`. Clean room: **T094_A_REPAIRABLE_GAP**.

**First exact failure:** signature-weighted pruning — normalized deficits stay \(O(1)\) on neutral corona nodes, preventing a positive-signature equality core as \(\epsilon\to0\).

**Secondary failure:** semicontinuity of retained-skeleton and sign-grouping deficits under core convergence.

T094 and T089R remain conjectural; no full-standard countermodel constructed.

---

## Tests

14 passed (D050) + 134 regression = **148 passed** (D050–D042 fast suite).

---

## Module inventory

Ten modules under `src/squarepeg/defect_extraction/`:

- `ledger_deficits.py`
- `corona_deficit_budget.py`
- `deficit_to_contraction.py`
- `deficit_distribution.py`
- `equality_core_pruning.py`
- `tree_core_selection.py`
- `equality_core_compactness.py`
- `deficit_semicontinuity.py`
- `t094a_repair.py`
- `t094a_clean_room.py`

---

## Next frontier

Close T096 by proving a tree density/pruning lemma forcing a deep coherent good subtree when \(\mathfrak D_L=o(\Phi)\), or close T095 on distributed positive deficit. Repair `NOT_CLOSED` deficits before claiming `T094_A_UNIFORM`.
