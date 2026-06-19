# Reference Annular Rhombus Component

## Model

Star-annular \(\Gamma_{\mathrm{ref}}\): \(R(t)\) alternates \(r_{\mathrm{inner}}=0.45\), \(r_{\mathrm{outer}}=1.0\) by quadrant.

## Rhombus family

\(z(t)=(t,t+\pi/2,t+\pi,t+3\pi/2)\), \(G_{\Gamma_{\mathrm{ref}}}(z(t))=0\).

| Property | Verified |
|----------|----------|
| \(\rank DG\) | 3 |
| Side margin | > 0.05 |
| Mod-2 normal degree | 1 |
| \(w_1(L_\chi)\) | 1 |
| T039 | **Applies** at \(\rho_{\mathrm{cyc}}\approx0.01\) |

Implementation: `reference_annulus.py`, `reference_rhombus_family.py`, `reference_cyclic_certificate.py`.
