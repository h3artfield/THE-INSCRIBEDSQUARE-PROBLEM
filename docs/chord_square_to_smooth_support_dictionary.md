# Chord Square → Smooth Support Dictionary

**Directive 012**

---

## Polygon certificate (exact)

Edge pattern: **(0, 3, 5, 0)** — two vertices on outer-arm edge 0.

| Slot | Poly edge | Edge param \(u\) | Chord endpoints (\(\theta\)) | Chord \(\theta\) of vertex |
|------|-----------|------------------|-------------------------------|----------------------------|
| 1 | 0 | `123574909883123382656/783176785809004249471` | \([\theta_0,\theta_0+\pi/2]\) | 6.531 |
| 2 | 3 | `515566058505096737446/2349530357427012748413` | \([\theta_0+3\pi/2,\theta_0+2\pi]\) | 11.340 |
| 3 | 5 | `700507479376466581385/783176785809004249471` | \([\theta_0+5\pi/2,\theta_0+3\pi]\) | 15.542 |
| 4 | 0 | `711993239270205241846/783176785809004249471` | \([\theta_0,\theta_0+\pi/2]\) | 7.711 |

**Geometric fact:** vertices lie in **chord interiors**, not on \(\gamma_+\) (F013).

---

## Smooth certified square (distinct from chord square)

All four vertices on **\(\gamma_+\)** at angles:

| Slot | \(J_i=[a_i,b_i]\) | Certified \(\theta_i\) |
|------|-------------------|------------------------|
| 1 | \([5.75,6.05]\) | 5.904665 |
| 2 | \([10.55,11.0]\) | 10.768443 |
| 3 | \([14.95,15.35]\) | 15.133643 |
| 4 | \([7.05,7.45]\) | 7.207559 |

Boundary order preserved; slots 1 and 4 on same arm, disjoint intervals.

---

## Parameter conventions

| Symbol | Meaning |
|--------|---------|
| \(u\) | Polygon edge parameter in \([0,1]\) |
| \(\theta\) | Spiral angle on \(\gamma_+\) or \(\gamma_-\) |
| \(t\) | Circle parameter \(r(\theta)/r(\theta_0)\) |

---

## Square vertex order

Cyclic boundary order: \(p_1\to p_2\to p_3\to p_4\) on \(\Gamma_{\mathrm{ds}}\).
