# Hull-Adjacent Geometric Ears — T058 (Directive 030)

## Hull adjacency

Gates \(g_i,g_j\) are **hull adjacent** when one boundary arc on \(\partial H(C)\) between them contains no other true gate.

## Weak-dual leaf theorem

A leaf of the weak dual determines a face with:
- gate-free boundary arc \(B_{ij}\);
- embedded graph path \(\Gamma_{ij}\) joining its endpoints.

Candidate ear boundary: \(\Gamma_{ij} \cup B_{ij}\).

## T058

Every finite saturated cluster with Jordan-disk hull, outerplanar \(G_C\), and \(\ge4\) gates contains a saturated geometric subcluster eligible for T051.

**Status.** PROVED_LOCALLY via `hull_adjacent_ear.audit_t058`.

Closes Directive 029 geometric-ear gap using **either** hull boundary arc (not just consecutive indices).
