# Smooth Square Interval Certificate

**Status:** CERTIFIED (Directive 012)

---

## Box

Radius \(0.15\) in \(\theta\)-space around `DISCOVERED_SMOOTH_THETA`.

Each \(J_i'\subset J_i\) (outer windows).

---

## Results

| Quantity | Bound |
|----------|-------|
| Side length LB | \(\ge 0.421\) |
| Min radius LB | \(\ge 0.248\) |
| Max \(|F|\) at center | \(<10^{-15}\) |
| det \(J\) | nonzero |
| Independent validator | pass |

Method: interval enclosure + Krawczyk + independent midpoint check.

---

## Certificate

`smooth_square_certificate.certify_discovered_root()`

Machine-readable JSON via `SmoothSquareExistenceCertificate.to_json()`.

---

## Verdict

**T025_PROVED_BY_DIRECT_INTERVAL_CERTIFICATE**
