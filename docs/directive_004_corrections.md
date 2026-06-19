# Directive 004 Corrections (Directive 005)

## 1. Midpoint value vs derivative

For \(g_*(x)=4x^3-6x^2+3x\):

| Quantity | Correct value |
|----------|---------------|
| \(g_*(1/2)\) | **1/2** |
| \(g_*(1/2)=0\) | **FALSE** |
| \(g_*'(1/2)\) | **0** |
| Collapse signature | **vanishing derivative**, not vanishing function |

Audit: no documentation asserts \(g_*(1/2)=0\). Historical Model-W PL witnesses used flat **grid values** near 1/2, not the cubic.

## 2. Derivative symmetry (F007)

\[
g_*'(x)=3(2x-1)^2=g_*'(1-x).
\]

The claim \(g_*'(1-x)\ne g_*'(x)\) in `artifacts/directive_004_report.md` was **false** — corrected.

**Updated synthetic conclusion:** The cubic is compatible with reflection symmetry at both action and derivative levels. Neither \(g(1-x)=1-g(x)\) nor \(g'(1-x)=g'(x)\) excludes \(g_*\).

## 3. Sublemma B.1 reclassification

Previously listed as next original theorem. Reclassified to **SOURCE_REPRODUCTION / CALIBRATION** per Directive 005.

## 4. Regression tests

`tests/test_cubic_symmetry_repair.py`
