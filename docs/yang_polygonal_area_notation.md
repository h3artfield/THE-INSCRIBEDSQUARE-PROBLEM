# Yang Polygonal Area Notation (YANG-AREA-v1)

**Source:** Danyu Yang, arXiv:1204.0112, pinned `data/sources/yang_1204.0112.pdf`  
**Status:** SOURCE NOTATION (Directive 008R)

---

## Partition

Finite partition of \([0,T]\):

\[
D=\{t_j\}_{j=0}^n,\quad 0=t_0<t_1<\cdots<t_n=T.
\]

**Mesh (Notation 2):**

\[
|D|:=\max_{0\le j\le n-1}|t_{j+1}-t_j|.
\]

---

## Piecewise-linear interpolant (Notation 9, eq. (4))

For continuous \(\gamma:[0,T]\to V\), \(\gamma^D\) agrees with \(\gamma\) on \(D\) and is **affine** on each \([t_j,t_{j+1}]\):

\[
\gamma^D(t)=\frac{t-t_j}{t_{j+1}-t_j}\gamma(t_{j+1})+\frac{t_{j+1}-t}{t_{j+1}-t_j}\gamma(t_j),
\qquad t\in[t_j,t_{j+1}].
\]

Defined on the full parameter interval \([0,T]\). Values on \(\Delta=\{(s,t):0\le s\le t\le T\}\) are generated from paths.

---

## Lie bracket and area (Definitions 12–14)

For \(\gamma_1,\gamma_2\in C^{1-var}\):

\[
A(\gamma_1,\gamma_2)(s,t)=\frac12\iint_{s<u_1<u_2<t}[d\gamma_1(u_1),d\gamma_2(u_2)].
\]

**Area of path:** \(A(\gamma):=A(\gamma,\gamma)\), valued in \([V,V]\) (antisymmetric tensor space, completion of \(\sum [v_i^1,v_i^2]\) with norm \(\|\cdot\|_{V\otimes V}\)).

**Normalization:** factor \(\mathbf{1/2}\) in the definition above.

**Bracket:** \([v_1,v_2]=v_1\otimes v_2-v_2\otimes v_1\).

---

## Area of PL approximant (page 10)

For partition \(D\subset[s,t]\):

\[
A(\gamma^D)(s,t)=\frac12\sum_{k,\,t_k\in D}[ \gamma(t_k),\gamma(t_{k+1})]-\frac12[\gamma(s),\gamma(t)].
\]

Defined for all \((s,t)\in\Delta\). On each subinterval where \(\gamma^D\) is linear, the area increment is determined by corner points.

---

## 1-variation on area

For \(\alpha:\triangle[0,T]\to [V,V]\),

\[
\|\alpha\|_{1-var,[0,T]}=\sup_D\sum_{k}\|\alpha(t_k,t_{k+1})\|
\]

(sup over finite partitions of \([0,T]\); see Yang (2) and Definition area closure (6)).

---

## Planar specialization (\(V=\mathbb R^2\), \(c=(x,\xi)\))

Scalar coefficient of \([e_x,e_\xi]\):

\[
[e_x,e_\xi] \text{ component of } [v,w] = x(w_\xi)-\xi(w_x).
\]

Repository implementation: `src/squarepeg/rough_area/yang_partition_area.py`.
