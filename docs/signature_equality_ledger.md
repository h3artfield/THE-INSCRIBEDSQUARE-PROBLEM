# Signature Equality Ledger (Directive 049)

Machine-readable ledger in `equality_ledger.py`. Every load-bearing inequality from attachment identity through T093:

| ID | Bound | Equality condition |
|----|-------|-------------------|
| WEDGE_PRODUCT | \|a∧b\| ≤ \|a\|\|b\| | orthogonality |
| TRIANGLE_NORM | \|a+b\| ≤ \|a\|+\|b\| | parallel same orientation |
| CAUCHY_SCHWARZ | \|⟨a,b⟩\| ≤ \|a\|\|b\| | collinearity |
| CHILD_INCREMENT | Φ(w) ≤ C Φ(v) | extremal scale ratio |
| HULL_DIAMETER | diam ≤ 2r | antipodal endpoints |
| CROSSCUT_AREA | A ≤ C L² | gate chord realization |
| RETAINED_SKELETON | m_ret ≤ m(v) | full child partition |
| MULTIGEN_PACKING | P_L ≤ (1-η)Φ | cov_L ≥ 0.25 signature-scale slice |

Each entry includes stability modulus ω(ε) in `equality_stability.py`.
