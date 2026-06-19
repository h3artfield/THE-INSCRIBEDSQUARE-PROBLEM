# Critical Variation Class Hierarchy

**Directive 008**

---

## Classes

| Class | Definition | Symbol |
|-------|------------|--------|
| **A** | Finite 2-variation | \(\|c\|_{2\text{-var}}<\infty\) |
| **B** | Vanishing 2-variation | \(\omega_2(c,\delta)\to 0\) |
| **C** | Enhancible | \(c\in\mathcal G_2(\mathbb R^2)\) |
| **D** | Critical modulus (T020) | \(\|c(t)-c(s)\|\le M|t-s|^{1/2}m(|t-s|)\), \(\int m^2/r<\infty\) |

---

## Valid implications

| Implication | Status |
|-------------|--------|
| D (on \([0,1]\)) \(\Rightarrow\) B | **PROVED_LOCALLY** (§8 T020) |
| D \(\Rightarrow\) C | **SOURCE** (Yang Thm 33) |
| C \(\Rightarrow\) B | **SOURCE** |
| B \(\Rightarrow\) C | **FALSE** (Yang counterexample) |
| A \(\Rightarrow\) B | **FALSE** (finite 2-var ≠ vanishing) |
| B \(\Rightarrow\) A | **FALSE** |
| T017 class (\(p<2\) finite p-var) \(\subset\) C | **SOURCE** (Yang: \(p<2\subset\mathcal G_2\)) |
| D \(\Rightarrow\) not in T017 | **CONJECTURAL** (needs exact-critical example) |

---

## T017 vs T020

T017: finite \(p\)-variation, \(p<2\) — **CLEAN_ROOM_VERIFIED** (frozen release).

T020: critical modulus — **CONJECTURAL_TARGET**; narrower than all finite 2-var.
