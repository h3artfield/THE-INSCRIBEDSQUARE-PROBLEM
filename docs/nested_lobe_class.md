# Nested Lobe Class \(\mathcal D_{\mathrm{nest}}\)

Quantitative parameters: \(\lambda_-,\lambda_+,\delta_{\mathrm{sep}},\beta\), depth \(m\).

A packet is in \(\mathcal D_{\mathrm{nest}}(m,\lambda_-,\lambda_+,\delta_{\mathrm{sep}},\beta)\) when it contains lobes \(L_1\supset\cdots\supset L_m\) with:

- Same orientation \(\sigma_{L_1}=\cdots=\sigma_{L_m}\)
- Scale control \(\lambda_- \le d_{L_{j+1}}/d_{L_j} \le \lambda_+\)
- Separation \(\delta_{\mathrm{sep}}\, d_{L_j}\) outside attachment corridors
- Area fullness \(a_{L_j} \ge \beta d_{L_j}^2\)

Implementation: `nested_chain.py`, `lobe.py`.

**Strengthened class (Directive 020):** add `ANNULAR_GRAPH` — bounded eccentricity and corridor width for packet-to-reference comparison.
