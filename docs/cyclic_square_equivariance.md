# Cyclic Square Equivariance

Cyclic relabeling:
\[
\tau(u_1,u_2,u_3,u_4)=(u_2,u_3,u_4,u_1).
\]

**Exact identities (every curve):**
\[
G_\gamma(\tau u)=A\,G_\gamma(u),\qquad
D_\gamma(\tau u)=-D_\gamma(u),
\]
with
\[
A=\begin{pmatrix}0&1&0\\0&0&1\\-1&-1&-1\end{pmatrix},\quad
A^4=I,\quad \det A=-1.
\]

**Consequence:** \(G_\gamma^{-1}(0)\) is \(\tau\)-invariant for every \(\gamma\).

The anti-equivariance of \(D\) is the central cyclic-odd structure.

Implementation: `cyclic_equivariance.py`.
