# Public API and boundary

The package exposes typed specifications and renderer functions from
`plot_foundation`. Submodules provide focused artists for lines, heatmaps,
surfaces, polarization, vectors, and analysis overlays.

Renderers accept NumPy-compatible arrays and caller-owned Matplotlib axes.
They do not read files, create directories, close figures, or infer domain
semantics. Use `profile_context()` for a scoped style profile and
`save_figure()` when a caller explicitly chooses an output path.

The package has no dependency on a simulator, DataFrame schema, registry, or
application-specific naming convention. Keep those mappings in the caller.
