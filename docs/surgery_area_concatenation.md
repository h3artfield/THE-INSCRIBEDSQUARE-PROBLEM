# Surgery Area Concatenation

**Directive 024 Part III.** Load-bearing identity.

## Relative area

\[
A_X(s,t) = \frac12 \int_s^t \bigl[(X_1(u)-X_1(s))\,dX_2(u) - (X_2(u)-X_2(s))\,dX_1(u)\bigr].
\]

Same convention as T021 / Liouville documents.

## Chen identity

For \(s < u < t\):

\[
A_X(s,t) = A_X(s,u) + A_X(u,t) + \frac12 \bigl(X(u)-X(s)\bigr) \wedge \bigl(X(t)-X(u)\bigr).
\]

Finite concatenation \(X = X^{(1)} * \cdots * X^{(m)}\): sum of component areas plus pairwise wedge terms.

Implementation: `concatenation_area.py`; verified in tests.
