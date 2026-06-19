# T017 Independent Proof Audit

**Date:** 2026-06-18  
**Auditors:** Analysis track + Source/application track (single document, two sections)

---

## Analysis audit

| Check | Result |
|-------|--------|
| Exponents \(p<q<2\) | ✓ Used consistently |
| Common parametrization \(S_n,P_n,c\) | ✓ T018 construction |
| Bézier \(C^1\) regularity | ✓ L2–L4 in smoothing doc |
| \(\|S_n-P_n\|_{1\text{-var}}\to 0\) | ✓ Sum of \(4r_v\) |
| Triangle: \(\|S_n-c\|_{q}\le\|S_n-P_n\|_{q}+\|P_n-c\|_{q}\) | ✓ |
| Young: \(1/q+1/q>1\) | ✓ for \(q<2\) |
| Periodic lift \(f_n(t+2\pi k)\) | ✓ |
| No numerical variation as proof | ✓ Tests are formula checks only |

**Pass.**

---

## Source / application audit

| Check | Result |
|-------|--------|
| AI-PEG-v3 version | v3 pinned, SHA verified |
| One-form | \(\lambda=\xi\,dx\) (§3 AI-PEG-v3) |
| Remark 5.6 / \(C^1\) sufficiency | \(C^1\) approximants permitted on measure-zero / approximation route |
| Thm 1.1 hypotheses | \(C^0\) + uniform primitive on compacts — met |
| Area normalization | \(\sqrt{\pi/A_n}\) scaling; primitive scales \(\lambda^2\) |
| Thm 4.1 / microlocal | Not reproved — imported via Thm 1.1 |

**Pass.**

---

## Residual risks (explicit)

- **T018 Jordan simplicity:** proof assumes sufficiently small disjoint corner disks — standard for simple polygons; formal topology left at textbook level.
- **BG Thm 2.2 on \(S^1\):** periodic identification handled by including \(0=1\) and fixed times; matches AI periodic lift.

---

## Verdict

Proof chain is complete subject to imported source theorems (BG, AI-PEG-v3). **Outcome A.**
