# Infinite Intrusion Trees (Directive 028)

## König extraction

For locally finite non-stabilizing intrusion trees, König's lemma yields either:

- an infinite nested intrusion ray \(C_1\supset C_2\supset\cdots\); or
- nodes of unbounded branching.

## Infinite nested ray

Record: spatial diameters, parameter intervals, gate count, sign/center sequences, area defect, annular vs multicenter geometry.

- Positive \(\limsup\) diameter → return to positive-scale / protected analysis.
- Vanishing diameter → maximal-parent cluster surgery may remove whole ray (open).

## Infinite branching

Branching mass \(B(C)=\sum_{\text{children}} \operatorname{diam}(C')^2\); signed-area variant tracked separately.

**Implementation.** `infinite_intrusion_tree.audit_infinite_intrusion_tree`, `example_infinite_ray_sequence`.

**Status.** CLASSIFICATION FORMALIZED; surgery closure CONJECTURAL.
