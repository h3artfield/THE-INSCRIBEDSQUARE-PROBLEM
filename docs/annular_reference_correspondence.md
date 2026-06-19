# Annular Reference Correspondence

**Directive 021 Parts VII–X.**

## Normalization

For selected layers \(L_j \supset L_k\):

1. Translate so \(c = 0\) (common-center regime).
2. Scale so \(\max_\theta r_j(\theta) = 1\).
3. Set \(g_* = \mathrm{median}_\theta\, r_k(\theta)/r_j(\theta)\).

Implementation: `normalize_layer_pair()`.

## Angular correspondence

\[
r_j(\theta) e^{i\theta} \longleftrightarrow e^{i\theta}, \qquad
r_k(\theta) e^{i\theta} \longleftrightarrow g_* e^{i\theta}.
\]

Four reference windows at \(\theta \in \{0, \pi/2, \pi, 3\pi/2\}\) match the star-annular \(\Gamma_{\mathrm{ref}}\) cyclic order (outer–inner–inner–outer).

Corridor handling: orientation-preserving angular parameter on \(S^1 \setminus \mathrm{corridors}\); corridor width bounded by \(w_{\mathrm{corr}}\).

Implementation: `build_radial_correspondence()`.

## Window order

The four packet windows retain the same cyclic order as the reference windows when annular-graph constants hold and layers share winding sign (`cyclic_order_preserved=True`).

## Reference model

Frozen in `artifacts/reference_annular_cyclic_certificate.json`:

- Outer \(\bar r_{\mathrm{out}}(\theta) = 1\), inner \(\bar r_{\mathrm{in}}(\theta) = g_* \approx 0.45\) outside corridors
- Two attachment corridors of width \(\le w_{\mathrm{corr}}\)
- Four certified support windows; cyclic ordering; T039 rank DG\(=3\), \(w_1=1\)
- Robustness radius \(\rho_{\mathrm{cyc}} \approx 0.0137\)

Source: `reference_annulus.star_annular_gamma()`, `reference_cyclic_certificate.certify_reference_annular()`.
