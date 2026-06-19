# Cluster Crosscut Surgery — T051 (Directive 028)

## Curved crosscut theorem

Any Jordan disk with two distinct boundary gates admits an embedded crosscut \(\sigma_C\) whose interior lies in the disk and avoids the retained curve. Construction: straight chord if valid; else collar arc or polygonal interior path.

**Implementation.** `cluster_crosscut.cluster_crosscut`, `prove_cluster_crosscut_exists`.

## T051 — Local Cluster Surgery

For two-gate clean cluster \(C\), replace the saturated subsystem by \(\sigma_C\).

**Claims (PROVED_LOCALLY):**

- resulting curve is Jordan (when packet isolation holds);
- uniform error \(O(\operatorname{diam}H(C))\);
- crosscut signature controlled;
- descendant intrusions removed simultaneously;
- compatible with T043R exact component decomposition (cluster treated as one maximal surgery packet).

**Implementation.** `cluster_crosscut.apply_cluster_surgery`.

**Status.** T051 — **PROVED_LOCALLY**.
