# L1 Block Signature (Directive 037)

`L1_BLOCK_SIGNATURE`:
- uniform local bound on \(S_n(\delta)\);
- \(\lim_N\lim_\delta\limsup_n\tau_{n,N}(\delta)=0\);
- blockwise T073;
- retained skeleton and crosscut tail control.

Limit order: limsup_n, then \(\delta\downarrow0\), then \(N\to\infty\).

**Implementation.** `block_tail_norm.py`
