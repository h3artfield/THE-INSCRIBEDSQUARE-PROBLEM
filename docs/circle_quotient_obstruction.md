# Circle Quotient Obstruction

## Ordered vs quotient configuration space

**Ordered space:** parameters \((\theta_1,\theta_2,\theta_3,\theta_4)\in(\mathbb R/2\pi)^4\) with period \(2\pi\) in \(t\).

**Cyclic quotient:** identify \(z(t)\sim z(t+\pi/2)\) by vertex relabeling. Fundamental domain length \(\pi/2\).

## Monodromy comparison

| Space | Period | Monodromy | \(w_1(E)\) |
|-------|--------|-----------|------------|
| Ordered | \(2\pi\) | +1 | 0 |
| Cyclic quotient | \(\pi/2\) | +1 | 0 |

**Verdict:** `QUOTIENT_OBSTRUCTION_TRIVIAL`

The obstruction line does **not** become nontrivial only after quotienting.

## Isotropy / closure

At \(t=\pi/2\), parameters are a cyclic shift of \(t=0\); the physical square repeats. The ordered family still closes at \(t=2\pi\) in parameter space.

Dihedral relabeling may flip orientation on coordinates; for this circle family it does not produce a nonzero \(w_1\) pairing.

Implementation: `circle_quotient.py`.
