# Normalized Gate Measure (Directive 031)

## Normalization

\(\widetilde H_n=(H(C_n)-z_n)/r_n\), \(\widetilde g_{n,i}=(g_{n,i}-z_n)/r_n\).

## Gate measure

\[
\nu_n=\frac1{M_n}\sum_i\delta_{\widetilde g_{n,i}}
\]

Compactness yields limit \(\nu_n\rightharpoonup\nu\).

Types: atomic, finitely supported, boundary arc, diffuse, multicenter.

**Implementation.** `normalized_gate_measure.py`
