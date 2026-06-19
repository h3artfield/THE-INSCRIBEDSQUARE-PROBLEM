# Intrinsic Nonsummable Order Tail (Directive 038)

## Decomposition-independent tail cost

For gate-order coupling \(\Pi_L\), let \(\mathfrak D(L)\) be measurable countable monotone decompositions
\(G(L)=\bigsqcup_{j\ge1}G^{(j)}(L)\) up to null sets.

For decomposition \(\mathcal D\):

\[
\mathcal T_{\mathcal D}(N,\delta)=\limsup_n\sup_{|J|\le\delta}\sum_{j>N}V_{n,j}(J).
\]

Optimal tail cost:

\[
\mathcal T_*(N,\delta)=\inf_{\mathcal D\in\mathfrak D(L)}\mathcal T_{\mathcal D}(N,\delta).
\]

The infimum is approximated over decompositions with block count \(>N\); attainment is not guaranteed.

## Intrinsic class

`NONSUMMABLE_ORDER_TAIL` when there exists \(\eta_0>0\) such that

\[
\lim_{\delta\downarrow0}\liminf_{N\to\infty}\mathcal T_*(N,\delta)\ge\eta_0.
\]

This definition does **not** depend on the T075 greedy decomposition.

**Implementation.** `intrinsic_order_tail.py`
