# T022 — Area-Tight Rectangular Peg Criterion

**Status:** PROVED_LOCALLY (Directive 010)

---

## Statement

If Jordan curve \(c\) admits an **area-tight** sequence of simple polygonal Jordan approximants, then \(c\) satisfies Asano–Ike Theorem 1.1 and inscribes every \(\theta\)-rectangle.

---

## Proof

1. **Equicontinuity of \(P_n\):** uniform convergence + Jordan modulus on \(S^1\).

2. **Primitive increment:**
   \[
   f_n(t)-f_n(s)=\frac{\xi_n(s)+\xi_n(t)}{2}(x_n(t)-x_n(s))-\mathcal A_{P_n}(s,t).
   \]

3. **Equicontinuity of \(f_n\):** coordinate bound \(M\) from uniform convergence; area-tightness kills \(\mathcal A_{P_n}\) on small scales.

4. **Arzelà–Ascoli:** extract \(f_{n_k}\to f\) uniformly on one period.

5. **T018 (frozen):** adaptive \(C^1\) \(S_k\) with primitive error \(<2^{-k}\).

6. **Period lift + AI-PEG-v3.**

Different subsequences may yield different \(f\); one suffices for Asano–Ike.

---

## Audit

`docs/t022_clean_room_audit.md`

---

## Recoveries

- **T019:** finite 2-var via T021 + local control \(\Rightarrow\) area-tight.
- **T020:** Yang all-partition Cauchy \(\Rightarrow\) area-tight (do not modify frozen T020 proof).
