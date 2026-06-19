# Smooth Double-Spiral Square System

**Directive 012**

---

## Map

\[
F(\theta_1,\ldots,\theta_4)=0
\]

with \(p_i=\gamma_+(\theta_i)\) on compact outer windows \(J_i\).

Square characterization: three equal edge lengths + equal diagonals.

Independent validator: midpoint \(p_1+p_3=p_2+p_4\) and rotation \(p_3-p_1=R_{90}(p_2-p_4)\).

---

## Implementation

`smooth_square_system.py`

---

## Certified root

`DISCOVERED_SMOOTH_THETA` — reconnaissance via mpmath Newton from chord-derived seed.

Side \(\approx 0.443\); all radii \(>0.24\).
