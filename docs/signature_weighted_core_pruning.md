# Signature-Weighted Core Pruning (Directive 050)

## Good nodes

Node \(u\) is ledger-good at tolerance \(\epsilon\) when \(\max_k d_k(u)\le\epsilon\).

## Markov bound

\[
\lambda_v\bigl(\mathcal W_L(v)\setminus\mathcal G_\epsilon\bigr)\ \le\ \frac{C}{\epsilon}\,\mathfrak D_L(v),
\]

using signature measure \(\lambda_v(\{u\})=\Phi(u)\), not node count.

## Observed gap

On tested neutral coronas, normalized deficits remain \(O(1)\) at parent signature scale (median \(d_k=1\)), so \(\mathcal G_\epsilon\) is empty for \(\epsilon<1\). Pruning is structurally correct but cannot yet produce a vanishing-\(\epsilon\) good set.

**Module:** `equality_core_pruning.py`
