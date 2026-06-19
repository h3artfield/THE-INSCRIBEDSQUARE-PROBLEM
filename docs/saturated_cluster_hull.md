# Saturated Cluster Hull (Directive 028)

## Definition

The **spatial saturation hull** \(H(L)\) is the smallest closed connected simply-connected region containing:

1. \(\Omega_L\);
2. all saturated intrusion arc images;
3. bounded complementary components required for simple connectivity.

This is **not** the convex hull. Implementation uses a radial boundary from the centroid to preserve local geometric scale.

## Properties

- If the intrusion system is spatially localized, \(\operatorname{diam}H(L)\) remains quantitatively small.
- Jordan disk failure is an explicit T050 alternative (`NON_JORDAN_HULL`).

**Implementation.** `saturation_hull.saturation_hull`.

**Status.** FORMALIZED; canonical refinement for proofs remains conjectural for overlapping hulls.
