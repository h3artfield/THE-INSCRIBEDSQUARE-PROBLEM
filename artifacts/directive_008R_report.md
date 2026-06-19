# Directive 008R Report — T020 Repair via Yang Universal Area Convergence

**Date:** 2026-06-18  
**Status:** COMPLETE

---

## Purpose

Reopen Directive 008 Outcome B and determine whether Yang Theorem 33 already proves convergence of \(A(c^D)\) for **all** fine partitions.

---

## Key finding

**F011 closed:** The Directive 008 gap misread Yang's proof. Theorem 33 establishes

\[
\|A(c^{D_1})-A(c^{D_2})\|_{1-var}\to 0
\]

for **all** pairs of partitions with mesh \(\le\delta\) (via Lemma 45 and the \(D_1\cup D_2\) argument in Theorem 23). Quantifier audit: **`ALL_PARTITIONS`**.

Boedihardjo–Geng polygons in \(\mathbb R^2\) **equal** Yang interpolants \(c^{D_n}\) as parametrized maps (straight chords, eq. (4)).

---

## Proof chain closed

| Step | Status |
|------|--------|
| Yang notation + Thm 23 quantifier | `docs/yang_theorem23_quantifier_audit.md` |
| Thm 33 Cauchy estimate | `docs/yang_theorem33_cauchy_estimate.md` |
| BG = Yang interpolant | `docs/bg_equals_yang_interpolant.md` |
| Area → Liouville primitive | `docs/critical_area_to_liouville_primitive.md` |
| Circle sign regression | `tests/test_circle_area_sign.py` |
| Adaptive T018 smoothing | `docs/critical_smoothing_primitive_control.md` |
| Clean-room audit | `docs/t020_clean_room_audit.md` |

---

## Verdict

### T020 — exactly one outcome

**Outcome A — T020 proved and audited**

```text
T020 — PROVED_LOCALLY_CLEAN_ROOM_VERIFIED
```

### T019

**STILL OPEN** (separate from T020 critical-modulus subclass).

---

## Historical record

Directive 008 Outcome B preserved in `artifacts/directive_008_report.md` — **not overwritten**.

---

## Tests

New tests: `test_yang_partition_quantifiers.py`, `test_liouville_area_identity.py`, `test_circle_area_sign.py`, `test_adaptive_smoothing_primitive.py`, `test_lifted_critical_primitive.py`.

Run: `python -m pytest tests/ -q`

---

## Acceptance checklist

- [x] Yang partition quantifier resolved (`ALL_PARTITIONS`)
- [x] Thm 33 Cauchy estimate reproduced
- [x] BG polygons = Yang interpolants (parametrized)
- [x] Liouville sign audited + regression
- [x] Area ⇒ uniform primitive on one period
- [x] Adaptive T018 with growing \(L_n\)
- [x] Lifted primitive template
- [x] Asano–Ike line-by-line (audit doc)
- [x] Clean-room audit complete
- [x] Outcome A selected
- [x] T019 separate — STILL OPEN
