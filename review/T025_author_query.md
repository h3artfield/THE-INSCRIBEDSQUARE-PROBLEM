# T025 Author Query

## For external reviewers (do not send without authorization)

1. Is corner evaluation of \(\det DF\) on a 0.15-radius box sufficient, or is full interval-arithmetic Jacobian required?
2. Does the boundary exclusion cover (170 adaptive cells) meet your standard for \(\partial B\) in \(\mathbb R^4\)?
3. Is the C⁰ homotopy degree argument standard for this square-map formulation?
4. Parameter order: confirm square vertex cycle vs boundary monotonic order is correctly documented.
5. Should \(\eta_0\approx 10^{-5}\) be improved before publication?

## Repository answers (internal)

- Det: all 16 hypercube corners same sign, interval width \(\approx 2.2\times10^{-4}\).
- Boundary: each terminal cell has one component strictly excluding 0; validator recomputes margin.
- Homotopy: uses only \(\|q_i-p_i\|_\infty\le\eta_0\), no derivatives.
- Order: audited in `docs/t025_parameter_order_dictionary.md`.
- Optimization: first valid certificate preserved; margin improved via adaptive refinement (013).
