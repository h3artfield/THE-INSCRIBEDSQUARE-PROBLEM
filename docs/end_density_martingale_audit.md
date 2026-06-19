# End Density Martingale Audit (Directive 047)

## Filtration

Tree cylinders generate the natural filtration for \(D_n(\xi)\).

## Classification

On tested singleton Cantor models, \(D_n\) is **not** a martingale (`classification=NONE`):

- cross-child mass defects are nonzero;
- \(\Phi_{\mathrm{end}}\) is non-additive across siblings;
- retained skeleton mass persists in parent cylinders.

## Defect terms

Explicit defects recorded: `mass_defect`, `phi_defect` per parent-child pair.

Any density-improvement proof must carry these correction terms; treating \(D_n\) as a martingale is invalid.

**Module:** `end_density_martingale.py`
