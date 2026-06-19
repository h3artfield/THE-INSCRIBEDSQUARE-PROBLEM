# Annular Packet Comparison Bound

**Directive 021 Part V.**

## Statement

For annular-graph packets normalized as in `annular_reference_correspondence.md`,

\[
\max_i \|p_i - q_i\|_\infty \le \Psi(K-1,\, L,\, g_+-g_-,\, w_{\mathrm{corr}},\, \delta_{\mathrm{core}}^{-1},\, \zeta).
\]

## Explicit decomposition

\[
\Psi \le C_1(K-1) + C_2 L \ell_{\mathrm{win}} + C_3(g_+-g_-) + C_4 w_{\mathrm{corr}} + C_5 \zeta + C_6 |g_* - g_{\mathrm{ref}}|
\]

with interval-certified coefficients in `PsiCoefficients`:

| Coef | Value | Source |
|------|-------|--------|
| \(C_1\) | 1.0 | After max-normalization, \(\|r-1\|_\infty \le 1-1/K \le K-1\) |
| \(C_2\) | 0.15 | Log-Lipschitz displacement across window arc \(\ell_{\mathrm{win}}=\pi/2\) |
| \(C_3\) | 0.35 | Radial gap spread vs reference annulus |
| \(C_4\) | 0.50 | Corridor angular width |
| \(C_5\) | 0.60 | Center drift |
| \(C_6\) | 0.40 | Median ratio deviation from reference \(g_{\mathrm{ref}}\) |

Implementation: `packet_reference_bound.psi_annular_bound()`.

## Certified regime

For the certified constants (\(K=1.005\), etc.):

\[
\Psi \approx 0.0118 < \rho_{\mathrm{cyc}} \approx 0.0137.
\]

Observed window distance on the example packet is \(\approx 0.005\), consistent with the bound.

## Open if regime widened

Widening \(K\) toward 1.01 without tightening \(\rho_{\mathrm{cyc}}\) leaves \(\Psi > \rho_{\mathrm{cyc}}\); the first obstruction is the eccentricity term \(C_1(K-1)\) at quadrant outer samples.
