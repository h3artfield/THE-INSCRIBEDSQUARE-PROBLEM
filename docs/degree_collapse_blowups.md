# Degree-Collapse Blow-Ups

**Status:** `FORMALIZED_DIAGNOSTIC` (Directive 014)

---

## Setup

When \(\rho_n\to0\), choose scale \(r_n\) from:

- square side length;
- minimum vertex separation;
- boundary margin;
- support-window diameter.

Rescale: \(z\mapsto (z-z_n)/r_n\).

---

## Local dichotomy target

Every degree-collapse blow-up either:

1. contains a protected square at rescaled level; or
2. has vanishing relative-area defect on bounded parameter windows.

This is a **local prototype** of T032 — not claimed for arbitrary Jordan tangents.

---

## Implementation

`blowup.py`: `choose_blowup_scale`, `analyze_blowup`, `local_dichotomy_prototype`.

Records rescaled side, rescaled area defect, branch classification.

---

## Use

Guide T033 failure-mode analysis; not a proof tool.
