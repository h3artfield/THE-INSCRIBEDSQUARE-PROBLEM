# T025 Parameter Order Dictionary

Reconnaissance display order \((5.90, 10.77, 15.13, 7.21)\) is **solver variable order**, not increasing boundary order.

---

## Exact mapping

| Variable | Spiral angle interval \(J_i\) | Boundary position (increasing \(\theta\) on \(\gamma_+\)) | Square vertex role in \(F\) |
| -------- | ----------------------------- | ----------------------------------------------------------- | --------------------------- |
| \(u_1\)  | \([5.75,\ 6.05]\)             | **1st** (first certified window)                            | \(p_1\) — edge \(p_1p_2\)   |
| \(u_2\)  | \([10.55,\ 11.0]\)            | **3rd**                                                     | \(p_2\) — edge \(p_2p_3\)   |
| \(u_3\)  | \([14.95,\ 15.35]\)           | **4th**                                                     | \(p_3\) — edge \(p_3p_4\)   |
| \(u_4\)  | \([7.05,\ 7.45]\)             | **2nd** (same arm as \(u_1\), disjoint interval)            | \(p_4\) — edge \(p_4p_1\)   |

---

## Square equations (variable order)

\[
F(u)=\bigl(
|p_1-p_2|^2-|p_2-p_3|^2,\ 
|p_2-p_3|^2-|p_3-p_4|^2,\ 
|p_3-p_4|^2-|p_4-p_1|^2,\ 
|p_1-p_3|^2-|p_2-p_4|^2
\bigr)
\]

where \(p_i = \gamma_+(u_i)\) with \(u_i\in J_i\).

---

## Boundary cyclic order vs square vertex order

Along the outer arm (increasing \(\theta\)):

\[
u_1 \;\to\; u_4 \;\to\; u_2 \;\to\; u_3
\]

Square vertex cycle in \(F\):

\[
p_1 \;\to\; p_2 \;\to\; p_3 \;\to\; p_4 \;\to\; p_1
\]

These differ: \(p_4\) appears before \(p_2\) along the curve, but \(p_2\) precedes \(p_4\) in the square edge cycle. This is valid — inscribed squares need not follow monotonic parameter order.

---

## Verification

Certified at \(\theta^\*=(5.9047,\ 10.7684,\ 15.1336,\ 7.2076)\).  
Boundary-order test: \(\theta^\*_1 < \theta^\*_4 < \theta^\*_2 < \theta^\*_3\).  
All intervals disjoint and contained in certified support windows.
