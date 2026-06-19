# Multi-Gate Ear Lemma — T056 (Directive 029)

## Two-gate ear

Subcluster \(E\subset C\) with:
1. Jordan-disk hull \(H(E)\);
2. attachment through exactly two gates;
3. retained curve avoids \(\operatorname{int}H(E)\);
4. contiguous parameter subsystem;
5. T051 crosscut exists.

## Graph vs geometric ear

| Level | Status |
|-------|--------|
| Graph-theoretic ear (leaf block / outermost chord) | PROVED_LOCALLY |
| Geometric saturated subcluster | Partial — hull-adjacent gates required |

## T056

Every finite outerplanar \(G_C\) contains a graph two-gate ear unless irreducible.

Geometric mapping may fail when graph leaf gates are not hull-adjacent (**Outcome B gap**).

## Ear removal

`EAR_REMOVAL_ORDER_DEPENDENT_BUT_TERMINATING` under canonical innermost-first order.

**Implementation.** `geometric_ear.audit_t056`, `ear_peeling.peel_ears`.
