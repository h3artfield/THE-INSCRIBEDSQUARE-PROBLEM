# Endpoint Multifunctions (Directive 046)

For an end \(\xi=(v_1,v_2\ldots)\), define nested hulls \(K_j(\xi)=\overline{H_{v_j}}\).

## Nesting audit

Classify: `END_HULLS_NESTED`, `END_HULLS_NESTED_AFTER_FILLING`, `END_HULLS_ONLY_EVENTUALLY_NESTED`, `END_HULLS_NOT_NESTED`.

## Compact-valued endpoint

When hulls are nested nonempty compact sets:

\[
\Phi(\xi)=\bigcap_{j\ge1}K_j(\xi).
\]

Properties proved locally: \(\Phi(\xi)\neq\varnothing\), compact; connected hulls imply connected \(\Phi\); \(\operatorname{diam}K_j\to0\) implies singleton \(\Phi\).

## Diameter classes

\(d_\Phi(\xi)=\operatorname{diam}\Phi(\xi)\), \(d_\infty(\xi)=\lim_j\operatorname{diam}K_j(\xi)\). Always \(d_\Phi\le d_\infty\).

Labels: `SINGLETON_END`, `ZERO_DIAMETER_END`, `CONTINUUM_END`, `POSITIVE_DIAMETER_END`.

**Module:** `endpoint_multifunction.py`
