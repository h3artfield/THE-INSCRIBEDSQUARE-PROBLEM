# Normalized Defect Blow-Ups

---

## Rescaling

\(r_k=\operatorname{diam}P_{n_k}(I_k)\), \(A_k(u)=(P_{n_k}(u)-z_k)/r_k\).

Normalized area may **diverge** as unscaled area stays \(\ge\varepsilon_0\) while \(r_k^2\to 0\).

---

## Absolute vs normalized robustness

Protected square of normalized radius \(c>0\) in \(A_k\) corresponds to absolute radius \(\sim c r_k\to 0\).

**Therefore:** local protected squares at shrinking scales do **not** contradict intrinsic global \(\rho_\square\to 0\).

**Do not** use blow-up square as limit square on \(\gamma\).

Implementation: `recursive_defect.normalized_blow_up`.
