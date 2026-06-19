# Critical Young Source Ledger (YANG-AREA-v1)

**Source:** Danyu Yang, arXiv:1204.0112  
**PDF:** `data/sources/yang_1204.0112.pdf`  
**SHA-256:** `b4bcea50e40a0e0da95d8d84cc9b8ea8660605b7d5fb011ab4b2b40b272b5a7d`  
**Retrieval:** 2026-06-18

---

## Key definitions

| Term | Yang notation |
|------|----------------|
| Finite 2-variation | \(C^{2-var}\) — sup over partitions of \((\sum|\Delta\gamma|^2)^{1/2}\) |
| Vanishing 2-variation | \(C^{0,2-var}\) — \(\omega_2(\gamma,\delta)\to 0\) as \(\delta\to 0\) |
| Enhancible | \(\gamma\in\mathcal G_2\) — admits geometric 2-rough enhancement |
| Area operator | \(A(\gamma^D)\) on piecewise linear approximants |

---

## Imported theorems

### Theorem 23 (Yang)

\(\gamma\in C^{0,2-var}\) **iff** \(A(\gamma^D)\) converges in **1-variation** as \(|D|\to 0\).

### Theorem 33 (Yang) — T020 modulus

If \(\|\gamma(t)-\gamma(s)\|\le C|t-s|^{1/2}m(|t-s|)\) with \(m(r)\to 0\), \(\int_0^1 m(r)^2/r\,dr<\infty\), then \(\gamma\in\mathcal G_2\).

### Theorem 29 (Yang) — critical Young

For paths with moduli \(m_1,m_2\) and \(\int_0^1 m_1(r)m_2(r)/r\,dr<\infty\), Young pairing at \(p^{-1}+q^{-1}=1\) extends.

---

## Counterexamples (source)

- **Vanishing 2-var ⊄ enhancible:** path \(f\) in Yang (Definition of f) has vanishing 2-var but area along partitions diverges.
- **Area operator not continuous** on 2-variation at critical exponent.

---

## T020 use (updated Directive 008R)

Yang Thm 33 proves **all-partition** Cauchy convergence of \(A(\gamma^D)\) in 1-variation. Combined with Thm 23 and BG chord = Yang \(\gamma^D\) in \(\mathbb R^2\), closes T020 polygonal step. See `docs/yang_theorem23_quantifier_audit.md`.
