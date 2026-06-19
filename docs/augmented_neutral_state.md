# Augmented Neutral State (Directive 051)

For each neutral node \(v\), state vector \(X(v)=(\Phi,R,S,J,C,B,G)\):

| Coordinate | Source |
|------------|--------|
| \(\Phi\) | end-signature scale |
| \(R\) | retained-skeleton reserve (`signature_budget.retained_skeleton`) |
| \(S\) | sign-grouping imbalance |
| \(J\) | wedge reserve (child-child + parent-child) |
| \(C\) | crosscut-area reserve |
| \(B\) | corona-boundary reserve |
| \(G\) | gate/center complexity |

Normalized state \(\widehat X = X/\Phi\) when \(\Phi>0\).

**Module:** `augmented_neutral_state.py`
