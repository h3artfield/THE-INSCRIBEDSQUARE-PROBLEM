# Signature-Controlled Surgery (T043R)

**Directive 024.** Replaces conjectural T043.

## T043R — Signature-Controlled Surgery-to-Area-Tightness

**Status:** CONJECTURAL_TARGET (hypothesis explicit; proof chain documented)

If \(P_n \to \gamma\) uniformly and maximal chord-safe forests satisfy `SIGNATURE_CARLESON`, then surgered \(Q_n \to \gamma\) uniformly and \((Q_n)\) is area-tight; T022 applies.

## Accumulated estimate

\[
\alpha_{Q_n}(\delta) \le \beta_n(\delta) + |A_{\mathrm{att},n}(\delta)| + C\,\omega_\gamma(\delta)\,\mu_{1,n}(\delta) + C\,\mu_{2,n}(\delta) + o_n(1).
\]

Under SIGNATURE_CARLESON, RHS \(\to 0\) (correct limsup quantifiers).

Implementation: `accumulated_surgery.py`.

## Simultaneous Jordan surgery

Maximal disjoint surgeries audited via `simultaneous_surgery_jordan()` — **not** Outcome E (no failure found).
