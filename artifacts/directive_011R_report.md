# Directive 011R Report — Compactness Audit

**Date:** 2026-06-18  
**Status:** Complete

---

## Verdicts

| Target | Outcome |
|--------|---------|
| **T025** | `T025_NOT_PROVED` (smooth \(\Gamma_{\mathrm{ds}}\)) |
| **T024-A** | `T024_A_RESTRICTED_CLASS_ONLY` |
| **T024-B** | `T024_B_STRONG_TOPOLOGY_ONLY` |

---

## T025 principal finding

Directive 011 misreported edges **\((0,3,5,4N+1)\)**. Actual macro certificate: **\((0,3,5,0)\)** with **literally identical** rational data for all \(N=3..7\).

* Infinite sequence exists (Route B): \(Q_N=Q\) for all \(N\ge 3\).
* Vertices lie on **outer-arm chords**, not on smooth \(\gamma_+\).
* Compactness to smooth curve **invalid**; `T025_PROVED_BY_COMPACTNESS` **withdrawn**.

---

## T024 principal finding

Smooth tail gives \(c_0>0\) limsup obstruction for **cyclic inscribed PL** sequences. Not proved for arbitrary PL or \(C^0\) primitive-convergent Asano–Ike approximants.

---

## Conclusion table (audited)

| Claim | Status |
|-------|--------|
| No area-tight cyclic BG-type polygons | **proved** (restricted class) |
| No area-tight arbitrary simple polygons | **not proved** |
| No primitive-convergent regular \(C^1\) under \(C^0\) AI route | **not proved** |
| Stable square for finitely many truncations | **superseded** — literal \(Q\) for all \(N\ge 3\) |
| Square for infinitely many truncations | **proved** (identical \(Q\)) |
| Square on canonical infinite smooth curve | **not proved** |
| Double spiral outside T022 | **proved** (T024-A) |
| Outside all AI approximation sequences | **not proved** (\(C^0\) open) |

**Narrowed conclusion:** area-tight method fails for stated PL class; smooth-curve square **unresolved**; do not claim conjecture failure or full AI route failure.

---

## T026

Formulated only — `docs/area_tight_or_square_dichotomy.md`

---

## Git

Directive 011 committed and tagged `directive-011-internal-2026-06-18`.
