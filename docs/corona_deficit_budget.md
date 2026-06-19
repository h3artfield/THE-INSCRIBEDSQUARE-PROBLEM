# Corona Deficit Budget (Directive 050)

## Corona window

\[
\mathcal W_L(v)=\{u\ge v:\ 0\le\mathrm{depth}(u)-\mathrm{depth}(v)<L\}.
\]

## Cumulative deficit

\[
\mathfrak D_L(v)=\sum_{u\in\mathcal W_L(v)} w_u\,\Delta(u),
\]

with window weight \(w_u=0.11\) matching the T093 ledger aggregation scale.

## Telescoping budget

Target one-sided inequality:

\[
\Phi(v)-P_L(v)\ \ge\ c\,\mathfrak D_L(v)-\mathrm{Boundary}_L(v)-\mathrm{Bad}_L(v),
\]

with \(c=0.15\). Boundary terms include:

- top/bottom corona slices (`boundary = 0.05 Φ`);
- bad-node exits (`bad = 0.02 Φ`);
- crosscut truncation and retained-skeleton corrections absorbed into \(\Delta\).

On tested binary/middle-thirds models, `budget_holds` is true at \(L=2\) when \(\mathfrak D_L=o(\Phi)\).

**Module:** `corona_deficit_budget.py`
