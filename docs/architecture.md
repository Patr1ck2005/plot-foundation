# Architecture

Plot Foundation is independent from both numerical analysis libraries and
consumer applications.

```text
consumer schema/workflow
        |
        v
consumer adapter -> plot_foundation typed models -> Matplotlib renderer
```

The package owns plot specifications, portable style policy, and rendering
primitives. Consumers own schema conversion, physical meaning, labels, output
directories, figure bundles, provenance sidecars, and decisions about which
plots belong in a workflow.

All grid renderers use x-first arrays with shape `(len(x), len(y))`. Vector
rendering receives explicit `u`, `v`, and optional color values; it does not
interpret Stokes parameters or infer a physical direction field.

Multi-surface rendering keeps z height, color values, alpha values, and direct
RGBA arrays as separate typed channels. Output and mesh export remain explicit
consumer operations; renderers do not write auxiliary files.

`eigenmode-analysis` and `plot-foundation` do not depend on one another. A
consumer may use either or both, and each package has an independent version
and release cadence.
