# Branch Edge Dictionary — Macro Square \((0,3,5,0)\)

**Directive 011R correction**

---

## Directive 011 error

Directive 011 reported edge indices **\((0,3,5,4N+1)\)**. Exact certificate inspection shows the macro branch is **\((0,3,5,0)\)** — two vertices on **outer-arm edge 0**.

Edge \(4N+1\) is a **fixed inner-arm chord** (not the macro branch support) for all \(N\).

---

## Edge dictionary for \((0,3,5,0)\)

| Slot | Index | Kind | Canonical geometry |
|------|-------|------|-------------------|
| 1 | 0 | outer arm | chord \(\gamma_+(\theta_0)\to\gamma_+(\theta_0+\pi/2)\) |
| 2 | 3 | outer arm | chord \(\gamma_+(\theta_0+3\pi/2)\to\gamma_+(\theta_0+2\pi)\) |
| 3 | 5 | outer arm | chord \(\gamma_+(\theta_0+5\pi/2)\to\gamma_+(\theta_0+3\pi)\) |
| 4 | 0 | outer arm | **same edge as slot 1** (two vertices on first outer chord) |

All four supports are **\(N\)-independent** for \(N\ge 3\) (extra turns append only beyond edge 5).

---

## Edge \(4N+1\) (not on macro branch)

| \(N\) | Index | Geometry |
|-------|-------|----------|
| any | \(4N+1\) | inner chord \(\gamma_-(\theta_0)\to\gamma_-(\theta_0+\pi/2)\) |

Fixed inner-arm piece; **not** the outer connector (that is edge \(4N+3\)).

---

## Literal certificate data (\(N=3..7\))

Parameters **identical** rationals:

```
t1 = 123574909883123382656/783176785809004249471
t2 = 515566058505096737446/2349530357427012748413
t3 = 700507479376466581385/783176785809004249471
t4 = 711993239270205241846/783176785809004249471
```

Vertices **identical**; side² **identical** for all \(N\in\{3,\ldots,10\}\).

This is **literal equality**, not numerical closeness.

---

## Smooth-curve gap

Vertices lie on **polygon chords**, not on smooth \(\gamma_+\) (verified: radial residual \(>0.2\)). Polygon inscription \(\neq\) smooth-curve inscription.
