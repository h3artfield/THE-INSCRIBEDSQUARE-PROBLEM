# Young Primitive Convergence

**Status:** PROVED_LOCALLY (Directive 006)

Primary proof: `docs/young_primitive_convergence_proof.md`

---

## Convention (AI-PEG-v3)

\(c_n=(x_n,\xi_n)\), Liouville \(\lambda=\xi\,dx\).

\[
f_n(t)-f_n(s)=\int_s^t \xi_n\,dx_n \quad\text{(Young / classical for }C^1 S_n\text{)}.
\]

---

## Result

If \(\|S_n-c\|_{q\text{-var}}\to 0\) uniformly on a common parametrization with \(q<2\), then \(f_n\to f\) uniformly on every compact subset of \(\mathbb R\) after periodic lift and area normalization.

---

## Implementation

`young_integral.py` — formula validation on polygonal graphs; not primary justification.
