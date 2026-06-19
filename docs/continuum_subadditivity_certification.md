# Continuum Subadditivity Certification

## Method

For PL g with breakpoints \(\{b_i\}\), define

\[
H(x,y) = g(x) + g(y) - g(x+y)
\]

on \(T = \{(x,y): x\ge0, y\ge0, x+y\le1\}\).

Partition \(T\) by lines \(x=b_i\), \(y=b_j\), \(x+y=b_k\). On each closed cell, \(H\) is affine in \((x,y)\); nonnegativity follows from nonnegativity at all cell vertices in \(T\).

## Implementation

`src/squarepeg/spectral_axioms/continuum_cells.py`

- `certify_pl_subadditivity(g) -> SubadditivityCertificate`
- Machine-readable: list of cells with coefficients \((a,b,c)\) and vertex minima

## Results

| Witness | Cells | min H | Status |
|---------|-------|-------|--------|
| g(x)=x (N=10 grid) | 55 | 0 | PASS |
| κ=11/10, N=40 | 820 | 0 | **PASS** |
| κ=11/10, N=160 | 12880 | −49/9600 | **FAIL** |

## Rejection of grid sampling

M=500 (or any finite) grid check is **discovery only**. Final acceptance requires cell certificate or analytic proof.

Directive 003 `verify_subadditive_grid(M=500)` is deprecated for certification purposes.

## Certificate format

JSON export available via `SubadditivityCertificate` dataclass fields: `ok`, `min_H`, `violations`, `cells`.

Each cell stores `(x_lo, x_hi, y_lo, y_hi, a, b, c)` with \(H(x,y)=ax+by+c\) on that cell.
