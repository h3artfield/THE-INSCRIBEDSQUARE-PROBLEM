# What is still missing for a universal inscribed-square proof?

Plain-language map of the gap. This is **not** a proof claim.

## The conjecture (one sentence)

Every simple closed curve in the plane has four distinct points that form a square with **nonzero** side length—not a collapsed diagonal.

## What we already have (big pieces)

1. **Exact finite lab** — On polygons we can find and *certify* squares with rational arithmetic; we know when the solver is complete on that class (T009).

2. **Benchmark curve** — On the canonical double spiral, analytic work shows **noncollapse**: some approximating sequence keeps squares with a **uniform minimum size** (spectral noncollapse note). That is **one curve**, not all Jordan curves.

3. **Proof-engineering spine** — On a certified Cantor tree *fixture*, hundreds of lemmas are proved locally: routes, collisions, positive-scale geometry, saturation hulls, parameter disconnection (Directives 042–061). That shows how obstructions **classify and route** on that model.

4. **Microlocal cleanup** — For Asano–Ike-style normal tests, the **outer annular kernel** can be removed uniformly (`r′ ≤ r/5`); the hard part is what remains inside the **truncated cone** paired with the **real spiral source** and target `G`.

## What is *not* done (the universal gap)

Think of three nested goals:

### A. Finish Option B on the double spiral (benchmark, not universal)

Still open on the analytic side:

- Build the **full ordinary-sheaf model** for the capped spiral (four cap branches, three levels, attaching maps—not one isolated epigraph).
- Compute **pushforward through the truncated cone** with those coefficients.
- Compute **pairing with the actual wild target** `G` and read off **kernel and cokernel** of the normal test.

Until that is done, even the **best concrete curve** in the program does not close the Floer/microlocal branch.

### B. T045R — from fixture logic to *every* Jordan curve

**T045R** (“universal protected-or-surgery extraction”) is the repo’s name for:  
*every* defect tree / end geometry either goes to solved surgery (T062, annular, finite-center, etc.) or to a **small named list of global obstructions*.

Status: **CONJECTURAL_FULL_EXTRACTION**.

What is missing:

- Prove the **extraction bridge** for arbitrary curves, not only the binary equal-ratio Cantor fixture.
- **Universalize** fixture-local wins (T103, T089E, T091-U, T112–T125, …) with explicit hypotheses—no silent “proved on fixture = proved everywhere.”
- Close or genuinely isolate the **global residuals** in the ledger:
  - `INFINITE_CENTER_GEOMETRY`
  - `NONSUMMABLE_DIFFUSE_END_GEOMETRY`
  - `T045R_UNIVERSAL_EXTRACTION_BRIDGE`
  - (and any geometry that still escapes after parameter/center/diffuse routes)

On the fixture, several former blockers are **routed or eliminated**; the ledger still lists them as **globally open** until universal theorems exist.

### C. Connect analysis to the Toeplitz statement for all Jordan curves

Even strong Floer/microlocal results on one curve **do not** automatically give:

- **Uniform noncollapse** of inscribed squares for **every** Jordan curve under **every** good approximating sequence.
- The **midpoint / spectral** route (Greene–Lobb style): a limit invariant with **positive slope at angle π/2** for **all** curves (T005 conjectural).
- The **restriction map** `r_C : M → N` on the collapsed diagonal (weaker target in `next-proof-idea.md`) for **all** curves—not just noncollapse on the spiral.

So the universal theorem needs **at least one** of:

- A proof that spectral / defect-tree / microlocal pipelines apply to **every** Jordan curve and force a **nondegenerate** square, or  
- A different geometric mechanism (e.g. uniform degree / configuration-space argument) that is proved for **all** curves, not only examples.

## One paragraph summary

We can **certify squares on polygons**, **classify obstructions on a certified tree model**, and **prove strong partial results on the double spiral**, including **removing outer kernel noise** in normal tests. We **cannot** yet: (1) complete the **inner spiral × cone × G** calculation on the benchmark; (2) **lift** fixture-local routing to **all** Jordan curves (T045R); (3) prove **every** Jordan curve has a **nondegenerate** square (Toeplitz). The conjecture remains **open**; the program narrows **where** a counterexample or the last lemma would have to live.
