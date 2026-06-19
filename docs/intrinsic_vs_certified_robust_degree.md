# Intrinsic vs Certified Robust Degree

Directive 015 separates three quantities:

| Symbol | Name | Meaning |
|--------|------|---------|
| \(\rho_\square(\gamma,B)\) | **Intrinsic box radius** | Exact mathematical supremum of \(C^0\) perturbation radii preserving protected-box status |
| \(\rho_\square(\gamma)\) | **Intrinsic curve invariant** | \(\sup_B \rho_\square(\gamma,B)\) |
| \(\underline\rho_k(P)\) | **Certified lower bound at level \(k\)** | Max radius certified by search at complexity \(\le k\) |
| \(\underline\rho_\infty(P)\) | **Certified limit** | \(\sup_k \underline\rho_k(P)\) |

## Inequality chain

\[
0 \le \underline\rho_k(P) \le \underline\rho_{k+1}(P) \le \rho_\square(P).
\]

Equality \(\underline\rho_\infty(P)=\rho_\square(P)\) for rational polygons **proved** under T034.

## Code naming

- `rho_square_certified_lower_bound_box` / `rho_square_certified_lower_bound_polygon`
- `intrinsic_rho_box`, `intrinsic_rho_curve`
- Never use `rho_square_cert` without `_certified_lower_bound` suffix

## Logical withdrawal (F014)

**Invalid:** certified radii \(\to 0\) implies area-tight subsequence.

**Valid (T032*):** intrinsic \(\rho_\square(P_{n_k})\to 0\) on compatible windows implies area-tight subsequence (conjectural).
