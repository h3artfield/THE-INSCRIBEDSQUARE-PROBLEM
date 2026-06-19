# T025 One-Page Summary

**Theorem T025:** The canonical double spiral \(\Gamma_{\mathrm{ds}}\) contains a nondegenerate inscribed square.

**Status:** `PROVED_LOCALLY_BY_DIRECT_INTERVAL_CERTIFICATE` — not externally verified.

---

## Exact statement

Four points on \(\gamma_+\) at parameters \(\theta_i\in J_i\) satisfy the square map \(F(\theta)=0\) with side length \(\ge 0.356\) and radius \(\ge 0.248\).

---

## Computer-assisted components

| Component | Method |
|-----------|--------|
| Root enclosure | Outward-rounded interval \(F(B)\ni0\) |
| Uniqueness | Krawczyk \(K(B)\subset\operatorname{int}(B)\) |
| Degree | \(\det DF(B)\) excludes 0; \(\deg=-1\) |
| Boundary | Adaptive face subdivision (170 cells) |

---

## Independent replay

Module: `independent_t025_verifier.py` + `iv_backend_v1.py`  
Verdict: **`T025_CERTIFICATE_REPLAYED`**

---

## Tag

`t025-smooth-double-spiral-internal-2026-06-18`

Do not send for external review without authorization.
