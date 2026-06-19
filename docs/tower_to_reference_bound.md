# Tower-to-Reference Bound

**Directive 022 Part VI.**

## Theta bound

\[
d_{\mathrm{win}}(\mathcal T, \mathcal T_{\mathrm{ref}}) \le \Theta
\]

Decomposition (`tower_reference_bound.py`):

- Per-level \(\Psi\) (Directive 021)
- Geometric series over depth: \(\sum \lambda^j \Psi\)
- Accumulated drift and phase terms

## Certified regime

For depth 3 reference tower: \(\Theta \approx 0.0113 > \rho_{\mathrm{tower}} \approx 0.0068\).

**Regime empty** for cross-scale transfer.

First open estimate: accumulated depth sum exceeds \(\rho_{\mathrm{tower}}\) even at minimal depth \(\ge 3\).
