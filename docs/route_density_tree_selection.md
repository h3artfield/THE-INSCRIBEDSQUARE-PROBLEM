# Route Density Tree Selection — T109 (Directive 057)

Descendant density:

[
D_r(v,n)=\frac{\sum_{u\ge v,\,\mathrm{depth}(u)=\mathrm{depth}(v)+n}\alpha_r(u)\Phi(u)}{\sum_{u\ge v,\,\mathrm{depth}(u)=\mathrm{depth}(v)+n}\Phi(u)}.
]

**Status:** PROVED_LOCALLY on tested fixture.

**Module:** `route_density_tree.py`
