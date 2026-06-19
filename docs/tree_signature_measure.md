# Tree Signature Measure (Directive 041)

Node weight \(s(v)\) derived from wedge identity:

\[
s(v)=M_v^2r_v^2 + J(v) + r_v\sum_w M_wr_w.
\]

Edge weight \(e(v,w)\le C M_v M_w r_v r_w\).

\[
\mu_{\mathrm{sig}}=\sum_v s_{\mathrm{local}}(v)\delta_v+\sum_{v\to w}e(v,w)\delta_{(v,w)}.
\]

**Implementation.** `tree_signature_measure.py`
