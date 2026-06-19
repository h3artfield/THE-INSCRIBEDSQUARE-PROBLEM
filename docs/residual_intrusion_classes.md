# Residual Intrusion Classes (Directive 028)

Directive 027 residual: `MULTICENTER_ALTERNATING_INTRUSION_TREE` (broad).

Directive 028 refines into explicit classes:

| Class | Defining conditions |
|-------|---------------------|
| `INFINITE_MULTIGATE_INTRUSION_RAY` | Non-stabilizing saturation; nested \(C_k\) with \(\operatorname{diam}\to0\) |
| `UNBOUNDED_BRANCHING_INTRUSION_TREE` | Unbounded local branching; \(B(C)\) unbounded |
| `NON_JORDAN_SATURATION_HULL` | \(H(C)\) fails Jordan disk classification |
| `DENSE_GATE_ACCUMULATION` | \(\ge4\) gates; alternating pairing; no T039 protection |
| `MULTICENTER_ALTERNATING_INTRUSION_TREE` | Fallback when not narrowed |

**Implementation.** `residual_classifier.classify_residual`.

Each class has explicit defining conditions; residual is **narrower** than Directive 027 whenever a refined class applies.
