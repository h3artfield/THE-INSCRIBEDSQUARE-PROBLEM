# T039 Cyclic-Odd Persistence

**Status:** `PROVED_LOCALLY` (Directive 019)

## Statement

A cyclic-odd protected rhombus component persists under parametrized \(C^0\) perturbations with \(\|\gamma-\gamma_0\|_\infty<\eta\).

## Proof chain

1. **Homotopy invariance** — `relative_rhombus_class.py`
2. **Quotient descent** — `quotient_continuation.py`
3. **Twisted-section zero** — `twisted_section_zero.py`
4. **Diagonal forces square** — \(G=0 \land D=0\)
5. **Continuous limit** — `continuous_curve_limit.py`

## Sufficient \(\eta\)

From \(m_G \approx 0.331\) and crude \(E_G(\eta)=12\eta\cdot\mathrm{diam}\): \(\eta \lesssim 0.014\).

## Remaining refinement

Sharp Lipschitz constants for \(E_G\) not fully certified (qualitative positive radius suffices).

Implementation: `t039_persistence.py`
