# T033 — Finite-Scale Dichotomy Target

**Status:** `FINITE_SCALE_DICHOTOMY_TARGET` (conjectural)

---

## Target statement

Normalize \(\operatorname{diam}(P)=1\). For fixed scales \(0<\delta<1\), \(\varepsilon>0\):

Every sufficiently fine simple polygon \(P\) satisfies at least one:

1. **Protected robust square:** \(\exists B\) with \(\rho_\square(P,B)\ge\varepsilon\);
2. **Small area defect:** \(\alpha_P(\delta)\le\Phi(\delta,\varepsilon)\) with \(\Phi\to0\) in the regime needed for compactness.

---

## Algebraic failure modes (Part VIII)

| Limiting type | Forces |
|---------------|--------|
| Side \(\to0\) | small relative area or rescaling |
| Parameter collision | family or collision |
| \(\det J\to0\) | rank drop |
| Isolated merge | rank-5 family |
| Boundary exit | window drift |
| Window drift | blow-up analysis |

Classification: `collapse_classifier.py`, `blowup.py`.

---

## Relation to T032

T033 is a **finite-scale** prototype; T032 is the **limiting selection** principle. Neither proved.

---

## Plausibility

Double spiral: T024 shows area-tight failure on cyclic PL class; T025/T027 show protected degree at fixed outer scale. Suggests branch (1) for that curve class without branch (2) on same sequence — consistent with T032 being false or requiring stronger hypotheses.
