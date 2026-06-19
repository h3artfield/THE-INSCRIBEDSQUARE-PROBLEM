# Order Interaction Concentration (Directive 038)

## Cross-block interaction measure

\[
\Xi_n=\sum_{i<j}\left|\tfrac12\sum_{\ell,k}\epsilon_{ij\ell k}\Delta_{i,\ell}\wedge\Delta_{j,k}\right|\delta_{(i,j)}.
\]

Spatial atoms record block-pair centers and weights (`InteractionAtom`).

## Tail signature density

\[
\Sigma_n(J;N)=\sum_{\max(i,j)>N}|A_{ij}(J)|.
\]

Failure of T073I is classified as:

- `LINEAR_MASS_NONSUMMABLE`
- `CROSS_SIGNATURE_NONSUMMABLE`
- `INTERNAL_BLOCK_NONSUMMABLE`
- `MULTIPLE_FAILURES`

## T076 — Nonsummable order-tail trichotomy

Every nonsummable positive-inversion Jordan lamination has a subsequence satisfying one of:

1. concentrated order interaction (T064/T064D);
2. finite-center order interaction (T062);
3. diffuse order-interaction limit;
4. infinite intrusion depth or non-Jordan saturation during normalization.

**Status.** `CONJECTURAL_STRUCTURAL_TARGET`; concentrated and finite-center branches classified locally.

**Implementation.** `order_interaction_measure.py`, `nonsummable_concentration.py`
