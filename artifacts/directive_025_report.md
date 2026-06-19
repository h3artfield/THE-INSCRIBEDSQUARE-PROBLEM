# Directive 025 Report — T043R Proof

**Date:** 2026-06-18  
**Verdict:** **Outcome C — T043R proved; attachment (2)-variation requires extra structure**

---

## Part I — Directive 024 frozen

Commit `86c7206`, manifest `f41e55d`, tag `directive-024-signature-surgery-internal-2026-06-18`.

---

## Part II–III — Exact master identity

\[
\mathbb A_{Q_n}(J)=\sum_i\mathbb A_{R_{n,i}}+\mathbb A_{Z_{n,J}}+\sum_i\mathbb A_{C_{n,i}}
\]

Boxed form with \(\mathbb A_Z=\frac12\sum_{i<j}\Delta_i\wedge\Delta_j\). Proved in `exact_component_decomposition.py`.

---

## Part IV–V — T043R proved

Under `SIGNATURE_CARLESON`: \(\alpha_{Q_n}(\delta)\le\beta_n+\sigma_n+\chi_n\to0\). Uniform convergence \(|Q_n-P_n|_\infty\le r_n^{\max}\).

**Status:** T043R **PROVED_LOCALLY**

---

## Part VI — Clean room

**T043R_CLEAN_ROOM_VERIFIED** (10/10 checklist)

---

## Part VII — Attachment (2)-variation

```text
ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE
```

Consecutive variation vanishes on circle-chord counterexample but true sup (2)-variation does not; T021 rescues **SIMPLE_SIGNATURE**.

---

## Part VIII — Practical classes

| Class | Implies SIGNATURE_CARLESON |
|-------|---------------------------|
| SIMPLE_SIGNATURE | sigma (partial) |
| BOUNDED_WINDING_SIGNATURE | sigma when \(r\to0\) |
| BOUNDED_MULTIPLICITY_SIGNATURE | sigma bound \(M(\pi/4)r^2\) |

---

## Part IX — T044R

Annular geometry \(\Rightarrow\) **bounded_local_multiplicity** only; full bridge **open** (Outcome B component).

---

## Reviewer checklist

All 10 items pass. T045 not attacked.

---

## Tests

28+ new tests; fast suite gate pending.
