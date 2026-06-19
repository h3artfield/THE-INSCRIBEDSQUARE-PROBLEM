# Directive 029 Report — Multi-Gate Ear Decomposition and Finite-Intrusion Extraction

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **B — Ear theorem proved; area allocation remains open**

---

## Executive summary

Directive 029 closes the **topological** finite multi-gate obstruction via outerplanar gate graphs, graph-theoretic two-gate ears, and recursive ear peeling. **T055** and **T056** (graph level) and **T057** (bounded-gate reduction without geometric gap) are proved locally. The **exact Chen join decomposition** is formalized, but the quantitative defect bound \(c(m)\) and full **T053B** extraction chain remain conjectural. Unbounded gate accumulation is separated into explicit residual classes.

---

## Part I — Directive 028 frozen

| Theorem | Status |
|---------|--------|
| T050 | CONJECTURAL_STRUCTURAL_TARGET |
| T051 | PROVED_LOCALLY |
| T052 | PROVED_LOCALLY |
| T053 | CONJECTURAL_TARGET |
| T054 | CONJECTURAL_MULTIGATE_TARGET |

Manifest: `artifacts/directive_028_verified_internal_manifest.json`.

Frozen proofs **not modified**.

---

## Part II–III — Gate word and outerplanarity

- Gate word \(W(C)\) with hull / parameter / retained orders (`gate_word.py`).
- Gate intervals distinguished by arc kind (no endpoint conflation).
- Intrusion gate graph \(G_C\) with explicit edge kinds.
- **T055 PROVED_LOCALLY:** noncrossing chord embedding => outerplanar.
- Block decomposition: blocks, cut vertices, bridges, leaf blocks.

---

## Part IV — Two-gate ears

- Two-gate ear axioms formalized (Jordan hull, two gates, T051 crosscut).
- **T056 PROVED_LOCALLY** at graph level (leaf blocks + outermost chords).
- **Geometric ear gap:** some graph leaves fail hull-adjacency isolation.
- Ear removal: `EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING` (innermost-first canonical order).

---

## Part V — Area allocation

Exact identity:
\[
\mathcal A_C = \mathcal A_E + \mathcal A_{C'} + \mathcal A_{\mathrm{join}}
\]
implemented via Chen wedges (`ear_area_allocation.py`).

Quantitative \(c(m)\) bound **not closed** — join signature may dominate (Outcome B).

---

## Part VI–VII — Ear peeling and T057

- Recursive peel terminates for outerplanar bounded-gate graphs.
- Jordan preservation when geometric ears validate.
- **T057 PROVED_LOCALLY** when peeling reaches two-gate forest (4-gate and nested 6-gate examples pass).

---

## Part VIII — T053B

- Certificate framework connects T057 → T052 → T043R.
- Status: `CONJECTURAL_CONTROLLED_EXTRACTION` (requires quantitative area allocation + retained-skeleton completeness).

---

## Part IX — Unbounded gates

Residual classes formalized:
- `UNBOUNDED_GATE_DENSITY_CLUSTER`
- `DENSE_BOUNDARY_GATE_ACCUMULATION`
- `UNBOUNDED_OUTERPLANAR_BRANCHING`
- `NONVANISHING_JOIN_SIGNATURE_CLUSTER`

Separated from finite-tree results.

---

## Part X–XI — Non-Jordan hulls and T050R

- Six obstruction types + repair classification.
- **T050R** five-branch classification replaces overstrong T050.

---

## Part XII — Falsification

| Test | Result |
|------|--------|
| 4-gate noncrossing matching | Outerplanar; peels to two-gate forest |
| 6-gate nested matching | Outermost ear found; peel terminates |
| Earless search | No counterexample in tested outerplanar family |
| Join-signature concentration | Detected by allocation audit |

No rational polygon found refuting T055. Geometric ear gap identified for non-adjacent graph leaves.

---

## Part XIII — Clean-room audit

| # | Question | Answer |
|---|----------|--------|
| 1 | Gate graph canonical? | Yes — from gate labels + arc kinds |
| 2 | Actually outerplanar? | Yes for noncrossing chords (T055) |
| 3 | Graph ear = geometric ear? | **No — partial gap** |
| 4 | Ear removal controlled? | Canonical order; terminating |
| 5 | Area allocation exact? | Yes (Chen); quantitative open |
| 6 | Bounded gate quantitative? | M_GATE_BOUNDED used in T057 |
| 7 | Jordan-preserving forest? | Yes when geometric ears valid |
| 8 | Retained-skeleton complete? | Partial — iteration on non-empty curves |
| 9 | Unbounded gates separated? | Yes — four residual classes |
| 10 | Non-Jordan classified? | Yes — six types |
| 11 | Interleaving unprotected? | Yes (T049) |
| 12 | T053B uses proved machinery? | Only T051/T052 where geometric ears pass |

---

## Part XIV — Outcome selection

**Outcome B:** Topological reduction (T055, T056 graph level, T057 peeling) works. Quantitative defect allocation and full T053B remain open.

---

## Theorem status after Directive 029

| ID | Status |
|----|--------|
| T055 | PROVED_LOCALLY |
| T056 | PROVED_LOCALLY (graph); geometric partial |
| T057 | PROVED_LOCALLY (no geometric gap) |
| T050R | CONJECTURAL_STRUCTURAL_TARGET |
| T053B | CONJECTURAL_CONTROLLED_EXTRACTION |

---

## Tests

```
tests/test_directive_029.py — 16 passed
```

Combined with Directive 028 regression: **26 passed**.

---

## Deliverables

All required modules under `src/squarepeg/defect_extraction/`, docs, manifest, and this report.
