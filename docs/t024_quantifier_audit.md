# T024 Quantifier Audit

**Directive 011R**

---

## Area-tightness (negation to prove)

\[
\exists c_0>0\;\forall\delta>0:\quad
\limsup_{n\to\infty}\sup_{d(s,t)\le\delta}|\mathcal A_{P_n}(s,t)|\ge c_0.
\]

---

## Smooth tail constant

For \(M_\delta\) with \(t(M_\delta)^2<\delta\) and \(N=M_\delta^2\):

\[
|\mathcal A_{\gamma_+}(M_\delta,N)|\ge\tfrac12\log M_\delta-C=:c(\delta)\to\infty\text{ as }\delta\downarrow 0.
\]

Choose \(c_0=\tfrac14\).

---

## Class ruled out (exact statement)

**T024-A — No area-tight cyclic inscribed polygonal interpolation sequence**

Class **(1–2):** simple polygons \(\Gamma_N\) or general \(P_n\to\Gamma_{\mathrm{ds}}\) uniformly with vertices in **cyclic parameter order** along the fixed circle parametrization, PL over cyclic partitions.

**Not proved for class (3–4):** arbitrary simple polygonal maps; arbitrary regular \(C^1\) Jordan maps under \(C^0\) convergence only.

---

## Transfer lemma

For each \(\delta\), choose \(M_\delta\). For any admissible sequence \((P_n)\), \(\exists n(\delta)\) such that polygonal relative area on tail interval \(I_\delta\) is within \(\tfrac12 c(\delta)\) of smooth value. Hence limsup \(\ge c_0\).

Endpoint chord \(\le r(M)^2=o(1)\). Winding stability needed only for annular refinement (optional strengthening).

---

## Verdict

```text
T024_A_RESTRICTED_CLASS_ONLY
```

Quantifiers match for **cyclic inscribed PL** class; not upgraded to arbitrary PL.

---

## Rename

Use full name: **T024-A — No area-tight cyclic inscribed polygonal interpolation sequence**
