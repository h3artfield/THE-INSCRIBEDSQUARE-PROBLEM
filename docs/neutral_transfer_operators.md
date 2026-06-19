# Neutral Transfer Operators (Directive 051)

Parent-child recursion:

\[
X(v) = E(v) + \sum_{w\in\mathrm{Ch}(v)} A(v,w)\,X(w).
\]

\(A(v,w)\) is diagonal with entry \(\Phi(w)/\Phi(v)\); \(E(v)\) carries wedge, crosscut, retained, and boundary terms from the attachment identity.

Admissible family \(\mathscr A\) classified by child count, scale ratio, gate type, and routed branches (concentration, positive scale, etc.).

**Modules:** `neutral_transfer_operator.py`, `transition_family.py`
