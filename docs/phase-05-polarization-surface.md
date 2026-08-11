# Phase 05: Polarization, Poincare, and surface rendering

Release: `0.1.4`

## Migrated renderers

This release promotes mature myPlots Matplotlib primitives into general,
schema-neutral functions:

- `render_polarization_ellipses`;
- `render_poincare_scatter`;
- `render_poincare_trajectory`;
- `render_surface_3d`.

All grid renderers use the established `(len(x), len(y))` data contract and do
not know about DataFrames, manifests, field names, or project paths. Consumer
adapters retain those concerns. Functions accept external axes and return the
same `RenderResult` used by line and heatmap rendering.

## Verification

- Plot Foundation: 16 passed.
- Tests use the Agg backend and close every figure after each test.
- Ellipse sampling count, equal aspect, Poincare 3D axes, trajectory segments,
  and xy-oriented surface rendering are characterized.

## Consumer rollout

myPlots will retain its Visualizer methods and route their extracted arrays to
these renderers. Workbench will map English-schema quantity payloads to the
same functions. The shared renderers never import eigenmode-analysis; numerical
Jones/Stokes conversion remains independently owned by that package.
