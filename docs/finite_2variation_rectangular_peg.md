# T019 — Finite-(2)-Variation Rectangular Peg Theorem

**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 009 Outcome A)

---

## Statement

Every Jordan curve \(c:S^1\to\mathbb R^2\) of **finite** 2-variation inscribes a \(\theta\)-rectangle for every \(\theta\in(0,\pi)\). In particular, it inscribes a square.

---

## Proof chain (Asano–Ike route)

1. **BG** simple Jordan polygons \(P_n=c^{D_n}\), mesh \(\to 0\), uniform convergence.
2. **T021** bounds polygonal relative areas by \(\frac\pi4\,\omega_c^2\).
3. **Local interpolation** controls \(\omega_{P_n}\) by \(\omega_c\).
4. **Primitive equicontinuity** of \(\{f_n\}\).
5. **Arzelà–Ascoli:** subsequence \(f_{n_k}\to f\) uniformly.
6. **T018 (frozen):** \(C^1\) Jordan \(S_k\) with primitive error \(<2^{-k}\).
7. **Period lift** on \(\mathbb R\).
8. **AI-PEG-v3 Thm 1.1 + Rem. 5.6.**

---

## Scope

- Requires **finite** 2-variation (not merely vanishing).
- Does **not** claim all Jordan curves.
- Internal synthesis; not externally peer-reviewed.

---

## Audit

`docs/t019_clean_room_audit.md`

---

## Dependencies

| Component | Source |
|-----------|--------|
| T021 | Local (this directive) |
| T018 | Frozen release |
| BG Thm 2.2 | Imported |
| AI-PEG-v3 | Imported |
