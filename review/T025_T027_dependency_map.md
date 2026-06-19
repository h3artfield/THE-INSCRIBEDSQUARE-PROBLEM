# T025 / T027 Dependency Map

```mermaid
flowchart TD
    CANON[Canonical double spiral] --> T025[T025 interval certificate]
    T025 --> FREEZE[013 freeze + replay]
    FREEZE --> DEG[Boundary degree cert]
    DEG --> T027[T027 C0 robustness]
    T027 --> T028[T028 wild tail]
    T024[T024 area obstruction] --> T026[T026 dichotomy conjecture]
    T025 --> T026
    T027 --> T026
    T022[T022 area-tight criterion] --> T026
```

## Layer summary

| Layer | Theorem | Status |
|-------|---------|--------|
| Existence | T025 | PROVED_LOCALLY |
| Replay | Independent verifier | REPLAYED |
| Degree | \(\deg(F,B,0)=-1\) | Certified |
| Robustness | T027 | PROVED_LOCALLY |
| Corollary | T028 | Corollary of T027 |
| Bridge | T026 | Conjectural |

PDF export: compile this file or use repository HTML renderer.
