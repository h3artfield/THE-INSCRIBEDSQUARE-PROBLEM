# Signature-Controlled Surgery (T043R)

**Directive 025.** Replaces conjectural T043.

## T043R — Signature-Controlled Surgery-to-Area-Tightness

**Status:** PROVED_LOCALLY

If \(P_n \to \gamma\) uniformly and maximal chord-safe forests satisfy `SIGNATURE_CARLESON`, then surgered \(Q_n \to \gamma\) uniformly and \((Q_n)\) is area-tight; T022 applies.

## Exact master identity (Directive 025)

\[
\mathbb A_{Q_n}(J)=\sum_i\mathbb A_{R_{n,i}}+\mathbb A_{Z_{n,J}}+\sum_i\mathbb A_{C_{n,i}}
\]

Straight chords: \(\mathbb A_{C}=0\), \(\chi_n\equiv0\).

## Area-tight estimate

\[
\alpha_{Q_n}(\delta)\le\beta_n(\delta)+\sigma_n(\delta)+\chi_n(\delta).
\]

Under SIGNATURE_CARLESON, \(\lim_{\delta\downarrow0}\limsup_n\alpha_{Q_n}(\delta)=0\).

Implementation: `t043r_proof.py`, `exact_component_decomposition.py`, `attachment_signature.py`.

## Clean room

**T043R_CLEAN_ROOM_VERIFIED** — `t043r_clean_room.py`.

## Attachment (2)-variation

`ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE`. Use `SIMPLE_SIGNATURE` or bounded winding/multiplicity.
