# Truncation Definition — \(\Gamma_N\)

**Status:** FROZEN (Directive 011R)

---

## Parameters

\(N\ge 3\) half-turns per arm; canonical \(\theta_0=2\pi\), \(\varepsilon=1/20\).

---

## Vertex list (CCW)

1. **Outer arm:** \(\gamma_+(\theta_0 + k\pi/2)\) for \(k=0,\ldots,2N\) — \(2N+1\) vertices.
2. **Origin:** \((0,0)\).
3. **Inner arm:** \(\gamma_-(\theta_0 + k\pi/2)\) for \(k=2N,\ldots,0\) — \(2N+1\) vertices.
4. **Connector endpoints:** \(p_-=\gamma_-(\theta_0)\), \(p_+=\gamma_+(\theta_0)\) (closes to vertex 0).

Total vertices: \(4N+5\). Rationalization: `Fraction.limit_denominator(1000)`.

---

## Edge classification

| Index range | Geometry | Artificial? |
|-------------|----------|-------------|
| \(0..2N\) | Outer-arm chords | no (chords of \(\gamma_+\)) |
| \(2N+1\) | Origin → inner outer sample | **yes** (truncation seam) |
| \(2N+2..4N+1\) | Inner-arm chords | no |
| \(4N+2\) | Inner last → \(p_-\) | **yes** (duplicate) |
| \(4N+3\) | Outer connector \(p_-\to p_+\) | no (permanent) |

---

## Uniform convergence

**Proposition.** \(\Gamma_N\to\Gamma_{\mathrm{ds}}\) uniformly in Hausdorff sense.

*Proof sketch.* Fix \(\epsilon>0\). Choose \(N\) large so outer samples cover \([\theta_0,\theta_0+2N\pi/2]\) with mesh \(\to 0\) on compact \(\theta\le T\). Extra turns only refine inner/outer tails toward origin. Artificial edges (origin seam, duplicate \(p_-\)) lie in \(\epsilon\)-neighborhood of \(\Gamma_{\mathrm{ds}}\) for \(N\ge N(\epsilon)\). Permanent connector is fixed. □

Code: `hausdorff_to_outer_arm(N)` gives explicit outer-arm chord error.

---

## Implementation

`canonical.py`, `truncated_spirals.py`, `truncation_audit.py`
