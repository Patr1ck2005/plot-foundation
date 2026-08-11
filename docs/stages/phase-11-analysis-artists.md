# Phase 11: selective analysis artists

Release 0.1.10 adds two domain-neutral artists that draw on caller-owned axes:

- Lorentzian/Fano comparison curves plus source scatter;
- preclassified `phi0`, `phi90`, and uncertain path segments.

myPlots retains fitting orchestration, physical interpretation, figure size,
fonts, `show`, saving, and output policy. No 3D parameter-space or PyVista
behavior moved in this phase. Tests use the Agg backend and close every figure.
