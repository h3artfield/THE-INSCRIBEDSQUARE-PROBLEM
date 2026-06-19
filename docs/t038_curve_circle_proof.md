# T038-Curve — Circle-Family Proof

## Statement

**T038-Curve (PROVED_LOCALLY):** There exists \(\eta_{\mathrm{circle}}>0\) such that every degree-one Jordan parametrization \(\gamma:S^1\to\mathbb R^2\) with \(\|\gamma-\gamma_0\|_\infty<\eta_{\mathrm{circle}}\) has a nondegenerate inscribed square with ordered parameters in \(U\).

## Proof ingredients

- Rhombus continuation (`rhombus_continuation.py`)
- Cyclic anti-equivariance \(D(\tau u)=-D(u)\) (`cyclic_equivariance.py`)
- Möbius sign line \(w_1(L_\chi)\ne0\) (`twisted_w1.py`)
- Collision/side margins in \(U\)
- Continuous limit (`continuous_curve_limit.py`)

## Not claimed

- Uniqueness of square
- Sharp quantitative \(\eta_{\mathrm{circle}}\) (qualitative \(\eta=0.01\) passes margin check)
- Full proof of abstract **T038′** (Euler cokernel bundle; still `CONJECTURAL_TARGET`)

## Relation to Directive 017

Curve-induced perturbations cannot realize arbitrary cokernel sections (Circle-B). The cyclic-odd sign line is a **different**, nontrivial bundle over the **quotient**.
