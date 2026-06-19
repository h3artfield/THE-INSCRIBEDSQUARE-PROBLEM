# T031 — Intrinsic Limit Criterion

---

## T031-A (certified)

If \(\limsup_n \underline\rho_k(P_n,B)>0\) on compatible certified boxes, limit curve has a square.

**Valid.** Does not imply T031-B.

---

## T031-B (intrinsic)

If \(\limsup_n \rho_\square(P_n)>0\) with compatible windows, limit curve has a square.

**Status:** PROVED_LOCALLY

**Proof:** Choose \(\eta>0\) and infinitely many \(n\) with \(\rho_\square(P_n,B)\ge\eta\). Uniform convergence on fixed \(B\) preserves boundary margin and separation. Limit inherits protected box; \(\rho_\square(\gamma,B)>0\); T030 gives square.

Implementation: `limit_persistence.t031_b_intrinsic_positive_limsup`.

---

## Do not infer T031-B from T031-A

Certificate failure at finite \(k\) does not show intrinsic radius zero (T034 gives equality only in limit \(k\to\infty\)).
