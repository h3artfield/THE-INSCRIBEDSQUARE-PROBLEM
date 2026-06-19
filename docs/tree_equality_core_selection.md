# Tree Equality-Core Selection — T096 (Directive 050)

## Coherent core types

| Type | Criterion |
|------|-----------|
| `GOOD_RAY_CORE` | depth ≥ 2, one child, coverage ≥ \(c_0/2\) |
| `GOOD_BUSHY_CORE` | depth ≥ 2, ≥ 2 children, coverage ≥ \(c_0\) |
| `GOOD_FINITE_BRANCH_CORE` | depth ≥ 1, coverage ≥ \(0.3 c_0\) |
| `GOOD_DISCONNECTED_SET` | good nodes without coherent ancestry |

**Coherent** means rooted subtree with compatible parameter/hull nesting and signature coverage \(\lambda_{v_n}(\mathcal K_n)\ge c_0\Phi(v_n)\).

## T096 status

`CONJECTURAL_SELECTION_TARGET` on tested models: no positive-signature coherent core at fixed \(\epsilon=0.12\) because pruning yields zero good signature mass.

## Tree density lemma (open)

Deep slice with signature fraction \(\ge c_0\) should force one of: deep good subtree, concentrated ray, finite-center decomposition, or boundary obstruction.

**Module:** `tree_core_selection.py`
