# Finite Intrusion Saturation — T050 (Directive 028)

## Metrics

For saturated cluster \(C\): depth \(d(C)\), branching \(b(C)\), node count \(N(C)\), gate alternation \(a(C)\), center count.

## T050 — Finite Intrusion Saturation Theorem

Every dirty polygonal lobe with **finite** intrusion tree satisfies exactly one:

1. full saturation is two-gate clean;
2. saturation reaches positive geometric scale;
3. retained curve meets hull through \(\ge4\) separated gates;
4. saturation hull fails Jordan disk (explicit planar obstruction graph).

**Status.** `CONJECTURAL_STRUCTURAL_TARGET`; finite-tree case **PROVED_LOCALLY** for small trees via leaf absorption induction.

**Implementation.** `finite_intrusion_tree.classify_finite_intrusion_tree`.

## Induction sketch

At each leaf: absorb intrusion, fill bounded complements, update outer boundary, track gates. Preserves two-gate structure or produces one of the four alternatives.
