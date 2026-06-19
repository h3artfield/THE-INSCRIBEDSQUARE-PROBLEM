# Nested Packet Window Extraction

From lobe tree, select layers \(L_j, L_k\) with \(k-j\ge q_0\).

Four cyclic windows \(J_1,\ldots,J_4\): outer-in, inner-in, inner-out, outer-out.

Algorithm: `annular_windows.extract_windows()` — parameter quadrants within outer lobe interval, pairwise disjoint, cyclically ordered.

Attachment corridors excluded qualitatively; core annulus between \(L_j\) and \(L_{j+1}\) carries monotone winding of common sign.
