# Countable Child Attachment Identity (Directive 042)

For finite truncation \(\operatorname{Ch}_N(v)\):

\[
\mathbb A_N(v)=\sum_{i=1}^N\mathbb A_{w_i}+\frac12\sum_{i<j}\Delta_{w_i}\wedge\Delta_{w_j}+\mathbb A_{\mathrm{parent/remainder},N}.
\]

\[
L(v)=\sum_i|\Delta_{w_i}|,\quad \tau_v(N)=\sum_{i>N}|\Delta_{w_i}|.
\]

Absolute convergence: \(\sum_{i<j}|\Delta_{w_i}\wedge\Delta_{w_j}|\le\frac12 L(v)^2\).

Tail estimate: \(\le L(v)\tau_v(N)+\frac12\tau_v(N)^2\).

**Implementation.** `countable_child_identity.py`
