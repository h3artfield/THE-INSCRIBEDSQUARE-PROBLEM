# Multi-Gate Cluster Classification — T054 (Directive 028)

## Four-or-more gates

If saturated cluster meets retained curve through \(2m\ge4\) ordered gates, record gate word on cluster boundary and parameter circle; track alternating vs nested pairing, center structure, winding signs, defect mass.

## Interleaving not protected

Directive 027 / T049: simple interleaving reference is **not** T039-protected. Multi-gate clusters are **not** auto-assigned to protected-square branch.

## T054 — Multi-Gate Cluster Classification

Positive-defect saturated cluster with \(\ge4\) external gates contains either:

1. two-gate subcluster carrying definite defect;
2. admissible protected square component (requires new theorem);
3. branching multicenter residual configuration.

**Status.** `CONJECTURAL_MULTIGATE_TARGET`.

**Examples.** `multigate_cluster.example_four_gate_cluster`, `example_six_gate_nested`.

**Implementation.** `multigate_cluster.audit_multigate_cluster`.
