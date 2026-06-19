# Continuum Countermodel Attempts

## Model S (strict bijection) — no valid countermodel found

| Class | Result |
|-------|--------|
| Finite strict PL | **Ruled out** by obstruction lemma |
| Finite PL + δ>0 LP | Minimum D_{N,k} > 0 for all tested δ>0 |
| Cubic/analytic perturbation of identity | g′(½)>0, D⁺>0 |
| Integral g(x)=∫w/∫w with w>0 | w(½)>0 ⇒ g′(½)>0 |
| Accumulating breakpoints at ½ | **UNRESOLVED** (limit not constructed) |

## Model W (nondecreasing) — one certified countermodel

**Function:** PL interpolation of N=40 grid LP witness at κ=11/10.

**Breakpoints:** x_i = i/40, i=0,…,40 (41 breakpoints).

**Properties proved:**

- g(0)=0, g(1)=1
- Nondecreasing (not strict)
- Lipschitz constant 11/10
- g(x+y) ≤ g(x)+g(y) on all of T (820-cell exact certificate)
- D⁺(g,½)=0 (flat segment [19/40, 21/40])

**Not proved:** Realizability as a Jordan Floer spectral invariant.

## Failed attempts

- N=160 PL witness: violates subadditivity on continuum (cell cert min H < 0)
- Naive plateau-then-rise: violates subadditivity (documented in Directive 003, confirmed)
- M=500 grid subadditivity: **not accepted** as continuum proof

## Refinement behavior

Grid LP optima at κ=11/10 stay 0 for N=40,80,160,320, but N=160+ PL extensions need independent subadditivity check — only N=40,80 pass cell certification in tested range.
