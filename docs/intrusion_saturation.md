# Intrusion Saturation (Directive 028)

## One-step saturation

\[
\mathcal S_1(L) = I_L \cup \bigcup_{K\in\text{intrusions}} I_K
\]
where each \(I_K\) is the **full** external parameter interval supporting the intrusion, not only the subarc geometrically inside \(\Omega_L\).

## Recursive saturation

\[
\mathcal S_{k+1}(L) = \mathcal S_k(L) \cup \{\text{intervals of intrusions into domains of }\mathcal S_k\},
\qquad
\mathcal S_\infty(L) = \bigcup_{k\ge0}\mathcal S_k(L).
\]

## Stabilization cases

| Case | Detection |
|------|-----------|
| Finite stabilization | \(\mathcal S_{k+1}=\mathcal S_k\) |
| Infinite nested | Non-stabilizing chain \(C_1\supset C_2\supset\cdots\) |
| Branching | Unbounded local fan-out |
| Macroscopic scale | \(\operatorname{diam}H(L)\) exceeds threshold |
| Seam wrap | Interval wraps parameter seam |

## Order independence

**Lemma.** Recursive saturation depends only on the intrusion tree, not processing order.

**Implementation.** `saturation.recursive_saturation`, `saturation_order_independent`.

**Status.** PROVED_LOCALLY (finite trees).
