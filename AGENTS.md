# Plot Foundation Agent Instructions

## Mission

Provide reusable, domain-neutral plotting specifications, style policy, and
backend renderers. The package must not know about a scientific domain,
simulator, DataFrame, manifest, registry, or consumer output workflow.

## Boundaries

- Public inputs are arrays and typed models.
- Renderers draw on caller-owned axes and never create directories or close figures.
- Saving requires an explicit path and never creates parent directories.
- Domain meaning and schema mapping remain in consumer adapters.
- Matplotlib global state must not be mutated at import time. Use scoped style
  contexts.
- New primitives require a consumer characterization case and package tests.

## Data-space decision invariant

Plot Foundation supplies views; it does not infer the caller's data model.
Before choosing a spec or renderer, classify intrinsic data dimension and
sampling topology, enumerate compatible views, and select the views required
by the task. Rendering dimension does not determine data dimension: a heatmap
and a 3D surface can represent the same 2D scalar grid. Use the canonical
[Data Space and Visualization Views](https://github.com/Patr1ck2005/plot-workflows/blob/main/docs/data-space-and-visualization.md)
specification and its six-field Agent decision record.

## Workflow

1. Characterize the required visual and artist contract in the caller.
2. Add a domain-neutral model and renderer behavior here.
3. Keep schema, output paths, and physical interpretation in caller adapters.
4. Record `runtime_info()` in acceptance provenance.
5. Update the public API document and run package tests.
6. Release a stable wheel; production callers do not use sibling path injection.
7. Keep the canonical data-space specification link in this Agent entry point.
