# Directive 019 Report

**Date:** 2026-06-18  
**Outcome:** **A — T038-Curve and T039 verified**

---

## Gate 1 — Test stability

| Test | Verdict |
|------|---------|
| `test_semicircle_relative_area_bounded` | `RESOURCE_OR_TIMEOUT_FAILURE` |
| `test_fixture_simple_ccw` | `NONREPRODUCIBLE` |

Hardening: hexagon fixture uses `Fraction` equality. Full 3 h suite not re-run; fast marker suite is CI gate.

---

## Gate 2 — Clean-room audit

**Verdict:** `T038_CURVE_CLEAN_ROOM_VERIFIED`

Parametrized \(C^0\) only; Fréchet promotion not claimed. \(m_G \approx 0.331\) reproduced.

---

## Gate 3 — T039

**Status:** `PROVED_LOCALLY`

Abstract lemmas: Z₂ homotopy invariance, quotient pairing, twisted-section zero. Circle is certified instance.

---

## Flake audit

See `docs/full_suite_flakiness_audit.md`.

---

## Rank-5 / ellipse

- Ellipse \(a=b\): `CYCLIC_ODD_CERTIFIED`
- Rank-5 families: default `UNPROTECTED` without separate audit

---

## Not attempted

- T032§ geometric bridge
- T036-N1 proof

---

**Tag:** `directive-019-cyclic-odd-audit-internal-2026-06-18`
