# Gate Density Parameter (Directive 031)

## Basic quantities

\[
M(C)=\#\operatorname{Gates}(C),\quad r(C)=\operatorname{diam}H(C),\quad \Lambda(C)=M(C)\,r(C)
\]

Refined: \(q(C)\le 3M(C)\), \(\Lambda_q(C)=q(C)\,r(C)\).

## Join bounds

\[
|\mathbb A_{\mathrm{join}}|\le C_0\,\Lambda_q^2\le C_1\,M^2 r^2
\]

Explicit: \(C_0=\tfrac12 C_{\mathrm{collar}}^2\), \(C_1=\tfrac{9}{2}C_{\mathrm{collar}}^2\).

## Dichotomy

| Regime | Condition |
|--------|-----------|
| **Sparse** | \(r\to0\), \(Mr\to0\) |
| **Dense** | \(r\to0\), \(\limsup Mr>0\) |
| **Bounded** | uniform \(M\le M_0\) (T053B) |
| **Positive scale** | \(\limsup r>0\) |

**Implementation.** `gate_density.py`
