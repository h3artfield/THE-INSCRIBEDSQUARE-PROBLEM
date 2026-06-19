# Critical Area to Liouville Primitive

**Status:** PROVED_LOCALLY (Directive 008R)  
**Convention:** AI-PEG-v3: \(c=(x,\xi)\), \(\lambda=\xi\,dx\).

---

## Antisymmetric scalar

Let \(a_c(s,t)\) be the \([e_x,e_\xi]\) coefficient of Yang's area \(A(c)(s,t)\):

\[
a_c(s,t)=\frac12\int_s^t\Bigl[(x(u)-x(s))\,d\xi(u)-(\xi(u)-\xi(s))\,dx(u)\Bigr].
\]

For PL \(c^{D}\) with partition points \(t_i\):

\[
a_c(t_i,t_j)=\frac12\sum_{k=i}^{j-1}(x_k\xi_{k+1}-\xi_k x_{k+1})-\frac12(x_i\xi_j-\xi_i x_j).
\]

---

## Recovery formula (integration by parts)

\[
\int_s^t \xi\,dx
=\frac{\xi(s)+\xi(t)}{2}\bigl(x(t)-x(s)\bigr)-a_c(s,t).
\]

**Sign check:** CCW unit circle \(c(t)=(\cos 2\pi t,\sin 2\pi t)\) on \([0,1]\):

- \(\oint \xi\,dx = -\pi\) (Green / AI orientation).
- Endpoint trapezoid vanishes; \(a_c(0,1)=\pi\); formula gives \(\int = -a_c(0,1)=-\pi\). ✓

Clockwise circle reverses both signs.

---

## Primitive

Normalize \(f(0)=0\):

\[
f(t)=\frac{\xi(0)+\xi(t)}{2}\bigl(x(t)-x(0)\bigr)-a_c(0,t).
\]

---

## Convergence

If \(P_n=c^{D_n}\), \(P_n\to c\) uniformly and \(A(P_n)\to\mathbb A_c\) in 1-variation, then \(a_{P_n}(0,t)\to a_c(0,t)\) uniformly on \([0,1]\) (1-var controls increment of area function). Hence \(f_n^P\to f\) uniformly.

**Implementation:** `src/squarepeg/rough_area/liouville_recovery.py`

---

## Do not identify

Rough area \(\mathbb A_c\) is **not** equal to \(\int\xi\,dx\) without the symmetric endpoint correction above.
