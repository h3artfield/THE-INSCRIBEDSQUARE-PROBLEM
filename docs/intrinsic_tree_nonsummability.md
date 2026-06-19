# Intrinsic Tree Nonsummability

Directive 043 defines intrinsic failure quantities independent of arbitrary truncation.

## Child nonsummability

For node \(v\) with children \(w_i\):

\[
\tau_v(N)=\sum_{i>N}|\Delta_{w_i}|,\qquad
\mathfrak N_{\mathrm{child}}(v)=\inf_{\text{compatible exhaustions}}\liminf_{N\to\infty}\tau_v(N).
\]

## Ray nonsummability

For ray \(v_1\to v_2\to\cdots\), intrinsic tail cost from cross-level wedges, crosscuts, and corrections.

## Tree nonsummability

\[
\mathfrak N_{\mathcal T}=\inf_{F_N}\liminf_{N\to\infty}\mu_{\mathrm{sig}}(\mathcal T\setminus F_N).
\]

## Failure classes

- `CHILD_LINEAR_NONSUMMABILITY`
- `CHILD_CROSS_SIGNATURE_NONSUMMABILITY`
- `RAY_SIGNATURE_NONSUMMABILITY`
- `DIFFUSE_END_NONSUMMABILITY`
- `MULTIPLE_TREE_FAILURES`

**Module:** `intrinsic_tree_nonsummability.py`
