# Directive 024 Report — Accumulated Surgery and T043R

**Date:** 2026-06-18  
**Verdict:** **Outcome C — Square-mass condition insufficient; T043R under strengthened SIGNATURE_CARLESON**

---

## Part I — Directive 023 frozen

`artifacts/directive_023_verified_internal_manifest.json` updated with `CHORD_SAFE_ISOLATED_PACKET` hypotheses and hashes.

---

## Part II — Corrected interpretation

Three quantities separated in docs and `area_change.py`. Removed false blanket \(O(r^2)\) for area **change**.

---

## Part III — Chen identity

**PROVED_LOCALLY** in `concatenation_area.py`; tests pass.

---

## Part IV–VI — Attachment chain and decomposition

Explicit \(\mu_1,\mu_2,V_{\mathrm{att},2},A_{\mathrm{att}}\); surgered subarc decomposition in `accumulated_surgery.py`.

---

## Part V — Square mass verdict

```text
SQUARE_MASS_INSUFFICIENT
```

Circle-chord counterexample: \(\mu_2 \to 0\), \(|A_{\mathrm{att}}| = \Omega(1)\).

---

## Part VII — T043R

`SIGNATURE_CARLESON` defined; T043 superseded by T043R (**CONJECTURAL_TARGET**).

Version B (attachment (2)-variation \(\to 0\)) implies signature locally.

---

## Part VIII — T044R

`ANNULAR_SURGERY_FOREST` defined; annular \(\Rightarrow\) signature **open**.

---

## Part IX — Extraction

T045, T032§ remain conjectural; not conflated with T043R.

---

## Part X — Reviewer checklist

| # | Answer |
|---|--------|
| 1 | Yes — three quantities separated |
| 2 | Yes — Chen sign verified |
| 3 | Yes — maximal packets |
| 4 | Yes — attachment chain included |
| 5 | **Rejected** — SQUARE_MASS_INSUFFICIENT |
| 6 | Yes — simultaneous Jordan audited |
| 7 | Yes — uniform error \(\le \max \operatorname{diam}D\) |
| 8 | Yes — correct limsup quantifiers in T043R statement |
| 9 | Yes — \(\beta_n\) non-circular |
| 10 | Yes — extraction open |

---

## Verdict

**Outcome C:** Rigorous counterexample to square-mass sufficiency; T043R stated under `SIGNATURE_CARLESON` (strengthened condition including attachment-chain vanishing).

---

## Code

7 new modules; 6 new test files (17 tests)
