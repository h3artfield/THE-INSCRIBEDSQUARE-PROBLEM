# Saturation Hull Geometry (Directive 060)

Curve-level saturation hulls are defined from intrusion-tree node geometry and gate-collision mass — independent of Cantor fixture encoding.

Each hull record carries: Jordan flag, boundary count, local connectivity, pinch detection, collision mass, and hull class (`JORDAN`, `NON_JORDAN`, `HARMLESS_QUOTIENT`).

**Module:** `saturation_hull.py`

**Status:** PROVED_LOCALLY on certified binary equal-ratio Cantor fixture (all nodes Jordan; harmless quotient artifacts separated).
