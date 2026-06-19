# Square Mass Sufficiency

**Directive 024 Part V.**

## Verdict

```text
SQUARE_MASS_INSUFFICIENT
```

## Counterexample

\(N\) equal chords on a unit circle: \(\mu_2(J) = N d^2 \sim 4\pi^2/N \to 0\) as \(N \to \infty\), but \(|A_{\mathrm{att}}(J)| = \Omega(1)\) (chain encloses disk).

Implementation: `square_mass_counterexample.py`.

## Fat-disk packing

Disjoint fat disks: \(\sum \operatorname{diam}^2 \le C(c_{\mathrm{fat}}) R^2\) in ball \(B(z,R)\) — controls mass, **not** attachment area directly.

Implementation: `fat_disk_packing.py`.
