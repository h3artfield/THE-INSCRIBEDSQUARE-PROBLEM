# Two-Gate Saturated Cluster (Directive 028)

## Saturated packet cluster

A cluster \(C\) comprises: saturated parameter subsystem, hull \(H(C)\), outer gates \(A_C,B_C\), retained-curve complement, intrusion tree.

## Two-gate clean

Generalizes `CHORD_SAFE_ISOLATED_PACKET`:

1. \(H(C)\) is a Jordan disk;
2. retained curve avoids \(\operatorname{int}H(C)\);
3. retained meets \(\partial H(C)\) only at \(A_C,B_C\);
4. full saturated cluster \(\subset H(C)\);
5. embedded crosscut \(\sigma_C:A_C\to B_C\) exists in \(H(C)\);
6. \(\operatorname{diam}H(C)\) quantitatively controlled.

**Implementation.** `two_gate_cluster.audit_two_gate_cluster`.

## Dirty ≠ unsurgerable

Example: bump lobe with single intrusion (`dirty_examples.example_dirty_saturatable_two_gate`) saturates to a two-gate clean cluster.

**Status.** PROVED_LOCALLY (audit + example).
