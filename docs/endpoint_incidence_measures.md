# Endpoint Incidence Measures (Directive 046)

## Why not arbitrary selection

A measurable selection \(s(\xi)\in\Phi(\xi)\) can artificially concentrate or disperse spatial mass; it is not canonical.

## Construction

Build joint incidence measure \(\eta\) on \(\operatorname{Graph}(\Phi)\) with \((\mathrm{proj}_{\partial\mathcal T})_\#\eta=\mu_{\mathrm{end}}\).

Disintegrate \(\eta(d\xi,dx)=\mu_{\mathrm{end}}(d\xi)\kappa_\xi(dx)\) using uniform probability kernels on \(\Phi(\xi)\) (shrinking-hull limit).

Spatial distribution: \(\nu_{\mathrm{space}}=(\mathrm{proj}_{\mathbb R^2})_\#\eta\).

**Independence audit:** `CANONICAL_INCIDENCE_MEASURE` relative to frozen tangent sequence.

**Modules:** `endpoint_incidence_measure.py`, `endpoint_kernel_disintegration.py`
