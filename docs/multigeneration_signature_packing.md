# Multigeneration Signature Packing — T093 (Directive 048)

Target (not one-step \(\theta<1\)):

\[
P_L(v)=\sum_{\substack{u\ge v\\ \mathrm{depth}(u)=\mathrm{depth}(v)+L}}\Phi(u)
\le (1-\eta)\Phi(v)
\]

for bounded \(L\) and \(\eta>0\), with descendant coverage \(\ge 25\%\) to exclude vacuous sums.

**Status:** PROVED_LOCALLY on tested Carleson singleton models; CONJECTURAL on non-Carleson residual.

## T093 descendant coverage (precise definition)

For node \(v\) and generation length \(L\), define:

\[
P_L(v)=\sum_{\substack{u\succ v\\ \mathrm{depth}(u)=\mathrm{depth}(v)+L}}\Phi_{\mathrm{end}}(u),
\qquad
\Phi_{\mathrm{desc}}(v)=\sum_{u\succ v}\Phi_{\mathrm{end}}(u).
\]

**Coverage** is the signature-scale fraction:

\[
\mathrm{cov}_L(v)=\frac{P_L(v)}{\Phi_{\mathrm{desc}}(v)}.
\]

T093 certificates require \(\mathrm{cov}_L(v)\ge 0.25\): the \(L\)-generation slice carries at least 25% of **total descendant signature scale** \(\Phi_{\mathrm{end}}\), not end mass \(M\) or defect mass.

The **uncovered signature mass** \(\Phi_{\mathrm{desc}}(v)-P_L(v)\) (plus neutral-corona mass not in contracting regions) must be tracked separately; it cannot silently carry persistent non-Carleson density. Residual mass enters long neutral coronas — the target of T094.

**Module:** `multigeneration_packing.py` (frozen by Directive 049)
