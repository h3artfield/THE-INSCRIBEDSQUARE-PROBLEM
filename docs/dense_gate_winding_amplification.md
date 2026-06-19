# Dense Gate Winding Amplification (Directive 032)

For dense sequences (\(\limsup M_n r_n \ge \lambda_0\), \(|\mathbb A_{C_n}|\ge\varepsilon_0\)):

\[
\mathbb A_{\widetilde Z_n} = \frac{\mathbb A_{Z_n}}{r_n^2} \ge \frac{\varepsilon_0}{r_n^2} \to \infty
\]

Hence \(|w_n|_{L^\infty} \gtrsim C_{\mathrm{iso}}|\mathbb A_{\widetilde Z_n}|\to\infty\).

Closing-chord correction uniformly bounded; cannot absorb blow-up.

Positive/negative masses \(W_n^+\), \(W_n^-\) — dominant sign carries fixed defect fraction.

**Implementation.** `winding_function.py`
