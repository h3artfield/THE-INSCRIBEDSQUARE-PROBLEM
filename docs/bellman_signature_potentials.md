# Bellman Signature Potentials (Directive 051)

Seek positive functional \(\mathcal B(X)=a\cdot X\) with

\[
\sum_{w\in\mathrm{Ch}(v)} \mathcal B(X(w)) \le (1-\eta)\mathcal B(X(v)), \quad \eta>0,
\]

and comparability \(c\Phi \le \mathcal B(X) \le C\Phi\).

Fallback: piecewise-linear \(\mathcal B=\max_j a_j\cdot X\).

T098 does **not** assume individual ledger deficits vanish.

**Module:** `bellman_potential.py`
