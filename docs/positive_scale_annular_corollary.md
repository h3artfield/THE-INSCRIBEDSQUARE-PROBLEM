# Positive-Scale Annular Corollary

**T036-N1-ANN-Corollary** — `PROVED_LOCALLY` (conditional on uniform packet regime)

## Statement

If an approximation sequence contains annular-graph defect packets with

\[
\limsup_n r_n > 0
\]

where \(r_n\) is the outer packet diameter, then a subsequence has inscribed squares with side length bounded below by \(c_{\mathrm{ann}} r_n\).

Under compatible parameter windows and uniform convergence of curve approximants, the limiting Jordan curve contains a nondegenerate square (T002 compactness).

## Compactness step

1. T036-N1-ANN gives \(\operatorname{side}(Q_n) \ge c_{\mathrm{ann}} r_n \ge c_{\mathrm{ann}} \varepsilon\) for some \(\varepsilon > 0\) on a subsequence.
2. Square vertices lie in a fixed compact set (curve approximants converge uniformly on \(S^1\)).
3. Extract convergent subsequence of square quadruples; limit gives inscribed square on limit curve (T002).

Implementation: `positive_scale_compactness.positive_scale_corollary()`.

## Packet-scale caveat

If \(r_n \to 0\), squares may collapse in original coordinates even though they exist at packet scale. This is **not** progress toward T032§ without cross-scale structure.
