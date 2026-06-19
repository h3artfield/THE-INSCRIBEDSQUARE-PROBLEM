# Parent-Child Signature Budget (Directive 048)

For node \(v\) with children \(w\):

\[
M(v)=\mu_{\mathrm{end}}([v]),\quad \Phi(v)=\Phi_{\mathrm{end}}(v),\quad P(v)=\sum_{w\in\mathrm{Ch}(v)}\Phi(w).
\]

Exact budget identity:

\[
\Phi(v)=P(v)+\mathcal E_{\mathrm{sep}}+\mathcal E_{\mathrm{join}}+\mathcal E_{\mathrm{crosscut}}+\mathcal E_{\mathrm{ret}}+\text{tails}.
\]

Terms derived from wedge algebra, crosscuts, and retained skeleton mass.

**Module:** `signature_budget.py`
