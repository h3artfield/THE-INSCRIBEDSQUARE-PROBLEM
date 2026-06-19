# Finite-PL Obstruction Lemma

**Status:** PROVED (conventional proof)

---

## Statement

Let \(g:[0,1]\to\mathbb{R}\) be a **strictly increasing** continuous piecewise-linear function with finitely many breakpoints. Then

\[
D^+(g, \tfrac12) > 0.
\]

---

## Proof

Write \(h = \tfrac12\) for brevity.

### Case 1: \(h\) lies in the interior of an affine segment

On an open interval \((a,b)\ni h\) we have \(g(x) = g(h) + m(x-h)\) with slope \(m > 0\) (strict increase).

For \(0 < \delta < \min(h-a, b-h)\) and \(|t| \le \delta\):

\[
\frac{g(h+t) - g(h-t)}{2t} = \frac{m(h+t) - m(h-t)}{2t} = m.
\]

Hence \(D_t(g,h) = m\) for all small \(t\), and \(D^+(g,h) = m > 0\).

### Case 2: \(h\) is a breakpoint

Let \(m_L > 0\) be the left derivative and \(m_R > 0\) the right derivative (strict increase on each adjacent segment).

For small \(t > 0\):

\[
g(h+t) - g(h-t) = m_R t + m_L t + o(t) = (m_L + m_R)t + o(t)
\]

so

\[
D_t(g,h) \to \frac{m_L + m_R}{2} > 0 \quad (t \downarrow 0).
\]

Therefore \(D^+(g,h) \ge (m_L+m_R)/2 > 0\).

∎

---

## Corollary

A **nondecreasing** finite PL function may have \(D^+(g,\tfrac12)=0\) if \(\tfrac12\) lies in a **flat** segment (slope \(0\)). This is Model W, not Model S.

---

## Implementation

`src/squarepeg/spectral_axioms/pl_obstruction.py` — `finite_pl_obstruction_holds`, `StrictPLFunction`.

Tests: `tests/test_finite_pl_obstruction.py`.

---

## Why Directive 003 reported \(D^+=0\)

The N=160 (and N=40) LP witnesses use **weak monotonicity** (\(G_{i+1}\ge G_i\)). The witness has **flat grid edges** at the midpoint (e.g. \(G_{79}=G_{80}=G_{81}\) at N=160), producing zero-slope PL segments containing \(x=\tfrac12\).

Directive 003 then:

1. Evaluated \(D_{N,1}\) at one grid window \(h=1/N\), not \(\limsup_{h\downarrow0}\).
2. Mislabeled the object as a strict continuum countermodel.
3. Used M=500 grid subadditivity instead of polyhedral cell certification.

The apparent \(D^+=0\) is **real for Model W** (flat segment) but **does not contradict** the obstruction lemma, which requires strict increase.
