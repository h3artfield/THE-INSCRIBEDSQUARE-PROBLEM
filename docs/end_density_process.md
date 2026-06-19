# End Density Process (Directive 047)

For each cylinder \([v]\), define intrinsic density:

\[
D(v)=\frac{\mu([v])}{\Phi_{\mathrm{end}}(v)}.
\]

Along an end \(\xi\), the filtration \(D_n(\xi)=D(v_n(\xi))\) tracks density down the ray prefix.

**Audit:** `end_density_process.py` verifies mass additivity across child cylinders and computes \(\liminf/\limsup\) density along boundary ends.

**Key finding:** child mass is not strictly additive; retained skeleton contributions prevent a naive martingale interpretation.
