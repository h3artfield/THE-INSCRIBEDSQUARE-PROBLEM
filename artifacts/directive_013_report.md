# Directive 013 Report — Freeze T025 and C⁰ Robust Square

**Date:** 2026-06-18  
**Status:** Complete

---

## Verdicts

| Item | Verdict |
|------|---------|
| T025 replay | `T025_CERTIFICATE_REPLAYED` |
| T027 | `T027_PROVED_LOCALLY_CLEAN_ROOM_VERIFIED` |
| T028 | `T028_PROVED_AS_COROLLARY` |

---

## Part I — Freeze T025

- Tag: `t025-smooth-double-spiral-internal-2026-06-18`
- Manifest: `artifacts/t025_verified_internal_manifest.json`
- Certificate: `artifacts/t025_smooth_square_certificate.json`
- Status: `T025 — PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE`

---

## Part II — Clean-room replay

- `independent_t025_verifier.py` + `iv_backend_v1.py` (no primary cert imports)
- Parameter order: `docs/t025_parameter_order_dictionary.md`

---

## Part III — Local degree

- \(\deg(F,B,0)=-1\)
- Boundary cover: 170 terminal cells, \(m\approx 9.0\times10^{-5}\)
- `artifacts/t025_boundary_exclusion_certificate.json`

---

## Part IV–V — T027 C⁰ robustness

- \(E(\eta)=2(8R\eta+4\eta^2)\), \(R\approx 0.423\)
- \(\eta_0\approx 1.1\times10^{-5}\), \(E(\eta_0)<m\)
- Side LB \(\ge 0.356\), separation preserved

---

## Part VI — T028 wild tail

Three examples in `wild_tail_examples.py`; square via T027, not root search.

---

## Part VII — Neighborhood comparison

| Neighborhood | Size |
|--------------|------|
| Krawczyk uniqueness | radius \(3/20\) in \(\theta\)-space |
| Degree box \(B\) | same |
| C⁰ perturbation \(\eta_0\) | \(\approx 1.1\times10^{-5}\) |
| Uniqueness after perturbation | not claimed |

---

## Part VIII — T026

Refined to nonzero-degree condition; remains conjectural. See `docs/t026_missing_universal_lemma.md`.

---

## Tests

14 new fast tests + legacy smooth certificate tests pass.

Not externally verified.
