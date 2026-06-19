# Half-Angle Triangle Inequality — Equality Audit

**Sources:** GL24b Prop. 3.6; GL26 §1; [11] Theorem 27 (cited in GL24b)

---

## Normalized scalar equality for g_*

\[
g_*\left(\tfrac12+\tfrac12\right) = g_*(1) = 1 = 2\cdot\tfrac12 = g_*\left(\tfrac12\right)+g_*\left(\tfrac12\right).
\]

Subadditivity factorization: \(H(\tfrac12,\tfrac12)=12\cdot\tfrac14\cdot\tfrac12\cdot 0=0\) — equality with **interior** contribution from factor \((1-x-y)=0\) at \(x+y=1\).

---

## Source triangle inequality (GL24b)

For smooth \(\gamma\), aspect ratio \(r\in(0,1/2]\), \(\theta_1+\theta_2\le\pi\):

\[
l_2(\gamma,r,\theta_1+\theta_2) \le l_2(\gamma,r,\theta_1) + l_2(\gamma,r,\theta_2).
\]

**Proof mechanism:** Floer product \(\star\) on \(\mathrm{JF}_2\); generator acts as unit in Morse-Bott limit as \(\theta\to0\) (GL24b Prop. 3.6).

---

## Questions

| # | Question | Answer |
|---|----------|--------|
| 1 | Which classes multiply? | \(\mathrm{JF}_2\) generator; product from [19] §3.9.1 |
| 2 | Product map | \(\star: \mathrm{HF}_k \otimes \mathrm{HF}_l \to \mathrm{HF}_{k+l-n}\); adapted to Jordan Floer |
| 3 | Equality implies about generators? | **NOT PROVED** in source for half-angle |
| 4 | Equality with diagonal approach? | **Possible** — equality at \(\theta_1=\theta_2=\pi/2\) does not preclude diagonal representatives in limit |
| 5 | Off-diagonal persistence forced? | **NOT PROVED** |
| 6 | Order-4 rigidity? | **NOT IN SOURCE** |
| 7 | Automatic from duality + endpoints? | **No** — g_* satisfies endpoints + duality + equality but is not spectral |
| 8 | Filtered product theorem needed? | **Candidate A** — see `docs/candidate_bridge_lemmas.md` |

---

## Is equality useless?

**For Level F alone:** Yes — g_* shows equality at \((\tfrac12,\tfrac12)\) is **compatible** with D⁺=0 and collapse profile.

**For Level S:** Unknown. Equality in **Floer product** may require representing cycles whose actions sum exactly; off-diagonal vs diagonal distinction is **not visible** in scalar \(g(x)\).

---

## Rigidity theorem status

**No equality-rigidity theorem** is stated or proved in this audit. Any such theorem must specify:

- filtered product defect;
- microlocal support away from diagonal;
- or barcode length at half-angle.

**Status:** CONJECTURAL (Candidate A).
