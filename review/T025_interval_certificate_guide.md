# T025 Interval Certificate Guide

## Files

| File | Purpose |
|------|---------|
| `artifacts/t025_smooth_square_certificate.json` | Full interval/Krawczyk data |
| `artifacts/t025_verified_internal_manifest.json` | Release metadata |
| `artifacts/t025_boundary_exclusion_certificate.json` | \(\partial B\) exclusion cover |

## Verification steps

1. Load rational box endpoints from manifest `root_box_endpoints`.
2. Reconstruct \(\gamma_+(\theta)\) from frozen formulas (no decimal centers).
3. Evaluate `F_interval` via outward rounding; confirm four components contain 0.
4. Evaluate `det_interval_on_box` at \(2^4\) corners; confirm exclusion of 0.
5. Run `replay_t025_certificate()` — expect `T025_CERTIFICATE_REPLAYED`.
6. Run `validate_boundary_certificate()` on boundary JSON.

## Interval software

- Primary (012): `smooth_square_intervals.py`
- Independent (013): `iv_backend_v1.py`
- Rounding: outward float enclosure

## Parameter order

See `docs/t025_parameter_order_dictionary.md`. Solver order \(\ne\) boundary monotonic order.
