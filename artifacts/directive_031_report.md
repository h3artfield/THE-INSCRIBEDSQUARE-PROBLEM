# Directive 031 Report — Unbounded Gate Density and the Sparse/Dense Gate Dichotomy

**Date:** 2026-06-18  
**Status:** Complete  
**Outcome:** **A — T060 proved**

---

## Executive summary

Directive 031 extends extraction beyond uniform gate bounds. The key parameter is \(\Lambda_n=M_n r_n\), not \(M_n\) alone. **T060** proves sparse unbounded-gate finite-intrusion extraction when \(M_n r_n\to0\). **T061** classifies the dense regime (\(\limsup M_n r_n>0\)). T045R remains conjectural.

---

## Part I — Directive 030 frozen

Manifest: `artifacts/directive_030_verified_internal_manifest.json`. T053B and prior proofs **not modified**.

---

## Part II–III — Gate complexity and join bounds

- \(\Lambda=M r\), \(\Lambda_q=q r\), \(q\le 3M\).
- \(|\mathbb A_{\mathrm{join}}|\le C_0\Lambda_q^2\le C_1 M^2 r^2\).
- \(C_0=0.5\), \(C_1=4.5\) (with \(C_{\mathrm{collar}}=1\)).

---

## Part IV — T060 sparse extraction

- \(M_n r_n\to0 \Rightarrow J_{M_n}(r_n)\to0\).
- Signed grouping: dominant sign class carries \(\ge\varepsilon_0/4\) (no \(1/M_n\) loss).
- **T060 PROVED_LOCALLY**.

Dense-gate clusters become the remaining finite-tree residual.

---

## Part V–IX — Dense regime

- Normalized gate measures \(\nu_n\rightharpoonup\nu\).
- Gate-word inversion: ordered vs scrambled.
- Block decomposition with cross-block join terms.
- T061 trichotomy: blocks / concentration / diffuse / multicenter.
- T062 controlled subclasses: ordered diffuse, finite-center.

---

## Part X — Separate residuals

- `INFINITE_INTRUSION_TREE` — not folded into dense-gate
- `NON_JORDAN_SATURATION_HULL`
- `POSITIVE_SCALE_NONANNULAR_CLUSTER`

---

## Part XI — Clean-room audit

| # | Answer |
|---|--------|
| 1 | \(Mr\) is correct join parameter |
| 2 | \(Mr\to0\) makes joins negligible |
| 3 | Signed grouping avoids \(1/M\) loss |
| 4–12 | Valid / separate / T045R conjectural |

**Verdict:** T060 clean; dense regime classified by T061.

---

## Part XII — Outcome

**Outcome A:** All finite-intrusion gate-sparse clusters reduced to surgery. Dense-gate clusters are the remaining finite-tree residual.

---

## Theorem status

| ID | Status |
|----|--------|
| T060 | PROVED_LOCALLY |
| T061 | PROVED_LOCALLY (classifier) |
| T062 | CONTROLLED_CLASS_TARGET / partial PROVED_LOCALLY |
| T045R | CONJECTURAL_FULL_EXTRACTION |

---

## Tests

14 passed (D031) + 12 passed (D030 regression).

---

## Deliverables

10 modules, 9 docs, manifest, this report.
