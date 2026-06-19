# Coherent Annular Tower

**Directive 022.** Quantitative definition of nested annular-graph packets embedded in a Jordan curve.

## Tower structure

Nested parameter intervals \(I_1 \supset I_2 \supset \cdots\) with annular-graph packets \(\mathcal P_j\) and outer scales \(r_1 > r_2 > \cdots \to 0\).

Implementation: `coherent_tower.py`.

## Hypotheses

| Constant | Meaning |
|----------|---------|
| \(\lambda_-,\lambda_+\) | Scale decay: \(\lambda_- \le r_{j+1}/r_j \le \lambda_+\) |
| \(C_{\mathrm{drift}}\) | Center drift: \(\|c_{j+1}-c_j\| \le C_{\mathrm{drift}} r_{j+1}\), \(c_j \to c_\infty\) |
| \(C_{\mathrm{phase}}\) | Corridor phase coherence (summable bound) |
| winding | Common orientation across levels |
| attachment | Child packet inside parent inner region without crossing outer windows |

Each level satisfies Directive 021 `ANNULAR_GRAPH` on its packet.

## Three scales (Part III)

1. **Packet scale:** square side \(\ge 0.12 r_j\) (T036-N1-ANN); collapses as \(r_j \to 0\).
2. **Tower outer scale:** \(r_1 > 0\); target fixed-scale theorem uses \(r_1\), not \(r_j\).
3. **Approximation scale:** tower must embed in limiting \(\Gamma\), not merely resemble polygonal chords.
