# T018 — Velocity-Matched Cubic Polygon Smoothing

**Status:** PROVED_LOCALLY_CLEAN_ROOM_VERIFIED (Directive 007R)  
**Supersedes:** quadratic Bézier construction (Directive 006)

---

## Theorem T018

For every simple polygonal Jordan map \(P:S^1\to\mathbb R^2\), every \(q\ge 1\), and every \(\varepsilon>0\), there exists a **regular** \(C^1\) Jordan map \(S:S^1\to\mathbb R^2\) with the same orientation and a **common** parametrization such that

\[
\|S-P\|_\infty<\varepsilon,\qquad \|S-P\|_{q\text{-var}}<\varepsilon.
\]

---

## Common parametrization at a corner

At vertex \(v=P(\tau)\), choose \(\delta>0\) and interval \(I_v=[\tau-\delta,\tau+\delta]\subset L\).

\[
A=P(\tau-\delta),\quad C=P(\tau+\delta),
\]
\[
u_-=\frac{v-A}{\delta},\quad u_+=\frac{C-v}{\delta},\quad L=2\delta.
\]

Polygon on \(I_v\): \(A\to v\to C\) with constant velocities \(u_-\), \(u_+\).

---

## Cubic Bézier controls

\[
Q_0=A,\quad Q_1=A+\tfrac23(v-A),\quad Q_2=C-\tfrac23(C-v),\quad Q_3=C.
\]

For \(s=(t-(\tau-\delta))/L\in[0,1]\):

\[
S(t)=(1-s)^3Q_0+3(1-s)^2sQ_1+3(1-s)s^2Q_2+s^3Q_3.
\]

Outside \(\bigcup_v I_v\): \(S=P\).

---

## Endpoint velocity matching (§4)

Cubic Bézier: \(\frac{dS}{ds}=3(Q_1-Q_0)\) at \(s=0\), \(\frac{dS}{ds}=3(Q_3-Q_2)\) at \(s=1\).

\[
\frac{dS}{dt}(\tau-\delta)=\frac{3(Q_1-Q_0)}{L}=\frac{2(v-A)}{2\delta}=u_-.
\]

\[
\frac{dS}{dt}(\tau+\delta)=\frac{3(Q_3-Q_2)}{L}=\frac{2(C-v)}{2\delta}=u_+.
\]

**Therefore \(S\) is \(C^1\)** at both splices under the shared parametrization (not merely \(G^1\)).

---

## Nonvanishing derivative and injectivity (§6)

Let \(a=v-A\), \(b=C-v\) (nonzero, not antiparallel after preprocessing).

\[
Q_1-Q_0=\tfrac23 a,\quad Q_2-Q_1=\tfrac13(a+b),\quad Q_3-Q_2=\tfrac23 b.
\]

Choose \(w=a/|a|+b/|b|\). Then \(w\cdot a>0\), \(w\cdot b>0\).

\[
\frac{dS}{ds}=3\bigl[(1-s)^2(Q_1-Q_0)+2(1-s)s(Q_2-Q_1)+s^2(Q_3-Q_2)\bigr]
\]

is a positive linear combination of \(Q_1-Q_0\), \(Q_2-Q_1\), \(Q_3-Q_2\) with coefficients summing to 3. Hence \(w\cdot dS/ds>0\) for all \(s\in[0,1]\).

Consequences: \(S'\neq 0\); \(w\cdot S\) strictly increasing on \(I_v\); cubic arc **injective**. Covers convex and reflex corners when \(a,b\) not antiparallel.

---

## Containment (§7)

Control points lie in \(\mathrm{conv}\{A,v,C\}\); Bézier curve lies in convex hull of controls. Arc does not meet open segments \((A,v)\), \((v,C)\) except endpoints (strict monotonicity in \(w\)-projection).

---

## Global Jordan simplicity (§8–9)

Choose disjoint disks \(D_v\) with \(\mathrm{conv}\{A,v,C\}\subset D_v\), meeting polygon only at incident edges. Basepoint on interior of an **unchanged** edge; seam not at smoothed corner.

---

## Variation estimate (§10–11)

Control polygon length \(\le |a|+|b|\). Hence \(\mathrm{Var}_1(S;I_v)\le |a|+|b|=\mathrm{Var}_1(P;I_v)\).

\[
\mathrm{Var}_1(S-P;I_v)\le 2(|a|+|b|)\le 4r_v
\]

when \(|a|,|b|\le r_v\). Sum over corners: \(\|S-P\|_{1\text{-var}}<\varepsilon\).

**q-variation:** For \(q\ge 1\), on any partition \(\Pi\),

\[
\Bigl(\sum_i|\Delta h_i|^q\Bigr)^{1/q}\le\sum_i|\Delta h_i|,
\]

so \(|h|_{q\text{-var}}\le|h|_{1\text{-var}}\). Thus \(\|S-P\|_{q\text{-var}}<\varepsilon\).

---

## Implementation

`src/squarepeg/variation/cubic_corner_smoothing.py`
