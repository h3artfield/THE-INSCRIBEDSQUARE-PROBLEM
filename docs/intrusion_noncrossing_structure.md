# Intrusion Noncrossing Structure (Directive 028)

## Intrusion components

For chord-closed lobe \(L\) with interval \(I_L=[a_L,b_L]\) and Jordan domain \(\Omega_L\), define
\[
E_L = S^1\setminus(a_L,b_L).
\]
An **intrusion component** is a connected component of \(P(E_L)\cap\operatorname{int}\Omega_L\).

Each component records: parameter interval \(I_K\), entry/exit contacts (lobe arc vs closing chord), orientation, chord-lobe decomposition, descendant intrusions.

## General position

Tangency, vertex contacts, overlapping chords, and zero-length components are removed by polygon subdivision and perturbation limits. The noncrossing theorem does **not** assume transverse intersection in the final statement.

## Noncrossing endpoint theorem

**Theorem (planar noncrossing).** Two disjoint embedded intrusion arcs in a Jordan disk have boundary contacts \(A_1,B_1,A_2,B_2\) whose cyclic order on a common projection axis is **nested** or **separated**, never interleaving (\(A_1,A_2,B_1,B_2\)).

**Implementation.** `intrusion_noncrossing.classify_endpoint_order`, `audit_noncrossing`.

## Planar graph

Compatible pairs form edges in the intrusion noncrossing graph; interleaving pairs are excluded from simultaneous embedding.

**Status.** PROVED_LOCALLY (endpoint projection test).
