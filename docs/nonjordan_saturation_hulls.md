# Non-Jordan Saturation Hulls (Directive 029)

## Obstruction types

- `PINCHED_BOUNDARY`
- `MULTIPLE_BOUNDARY_COMPONENTS`
- `TOUCHING_COMPLEMENTARY`
- `DENSE_BOUNDARY_CONTACTS`
- `DISCONNECTED_INTERIOR`
- `SEAM_ARTIFACT`

## Repair

Some failures repairable by filling bounded complementary components; others genuine obstructions.

Prime-end formulation deferred unless crosscut theorem sourced.

**Implementation.** `nonjordan_hull.classify_hull`.
