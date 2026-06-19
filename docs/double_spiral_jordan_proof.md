# Double Spiral — Jordan Proof Sketch

**Status:** PROVED_LOCALLY (Directive 010)

---

## Injectivity

- Each arm is strictly monotone in \(\theta\) with \(r(\theta)>0\) for \(\theta\ge\theta_0\), hence injective.
- \(d(\theta)>0\) and \(d(\theta)=o(r(\theta))\) for large \(\theta\) \(\Rightarrow\) arms disjoint away from \(0\).
- Inner turns lie strictly inside outer annuli between consecutive half-turns (separation \(d(\theta)\)).
- Origin is the unique accumulation point; compactified parametrization continuous at \(0\).
- Removing any point leaves an arc (standard Jordan curve at origin pinch).

---

## Not from rendering

Arguments use explicit separation bounds \(d(\theta)\) and monotonicity of \(r\).

See `tests/test_double_spiral_separation.py`.
