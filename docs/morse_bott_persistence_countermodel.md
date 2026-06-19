# Morse–Bott Persistence Countermodel

## Map

\[
F:\mathbb R^2\to\mathbb R^2,\qquad F(x,y)=(x,0).
\]

## Zero set

\[
Z=\{(0,y):y\in\mathbb R\}.
\]

## Verified properties

| Property | Value |
|----------|-------|
| \(\dim Z\) | 1 (smooth submanifold) |
| \(\ker DF\) | \(\mathrm{span}(e_y)=T_zZ\) |
| Normal (\(x\)) derivative | 1 — isomorphism in normal direction |
| Fiberwise normal degree | nonzero (1D) |

## Perturbation

For every \(\varepsilon\ne0\),

\[
F_\varepsilon(x,y)=(x,\varepsilon)
\]

has **empty** zero set.

## Conclusion

> Normal nondegeneracy or a nonzero fiberwise normal degree does **not** alone imply persistence of a positive-dimensional zero family under arbitrary small \(C^0\) perturbations.

The missing data is the **cokernel obstruction** in the \(y\)-direction: a constant nonzero section of \(\operatorname{coker}(DF)\) removes all zeros.

Implementation: `morse_bott_countermodel.py`.
