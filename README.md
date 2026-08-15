# Plot Foundation

`plot-foundation` is a domain-neutral plotting library for typed plot
specifications, scoped style policy, and Matplotlib renderers. It does not
depend on a consumer's schema, file format, or workflow objects.

The library supports plain lines, scatter series, filled ribbons, color-mapped
lines, heatmaps/contours, simple and multi-layer 3D surfaces, polarization/Poincare primitives,
and explicit x-first vector/director fields. Renderers can create a figure or
draw on caller-owned axes, but they never save, close, or create directories.
Saving is a separate, explicit operation.

Shared profiles separate analysis and publication output:

- `diagnostic`: titles, labels, legends, grids, larger consumer-selected
  geometry, and 150 DPI;
- `publication_minimal`: A-derived minimal presentation, compact semantic
  presets, transparent tight-cropped output, and 300 DPI;
- `preview`: minimal publication presentation at 150 DPI;
- `paper`: backwards-compatible alias of `publication_minimal`.

Apply profiles through `profile_context()` and `save_figure()`; do not mutate
global `rcParams`. Aspect, limits, normalization, and colormaps remain explicit
physical inputs rather than profile constants.

The current release includes line, scatter, heatmap, contour, surface,
polarization, vector-field, lineshape, and field-regime artists. Figure
creation, saving, and physical interpretation remain explicit caller policy.

Before selecting one of these views, classify intrinsic data dimension and
sampling topology using the canonical
[Data Space and Visualization Views](https://github.com/Patr1ck2005/plot-workflows/blob/main/docs/data-space-and-visualization.md)
specification. A surface renderer consumes a 2D `z = f(x, y)` object; it does
not imply dense 3D data.

```python
from plot_foundation import (
    AxesSpec,
    LinePlotSpec,
    LineSeries,
    SeriesStyle,
    render_line_plot,
)

spec = LinePlotSpec(
    series=(LineSeries([0, 1], [1, 2], style=SeriesStyle(color="black")),),
    axes=AxesSpec(xlabel="x", ylabel="y"),
)
result = render_line_plot(spec)
```

For a non-square vector field:

```python
from plot_foundation import VectorFieldPlotSpec, render_vector_field

result = render_vector_field(
    VectorFieldPlotSpec(x=x, y=y, u=u, v=v, color_values=color)
)
```

Grid arrays always have shape `(len(x), len(y))`; transposed consumer payloads
must be adapted explicitly at the consumer boundary.

Multi-surface layers keep height, color, alpha, and RGBA channels independent;
NaNs create holes without changing the physical height scale or writing mesh
files as a hidden side effect.

See [the architecture](docs/architecture.md), [style policy](docs/style-policy.md),
and [line-rendering contract](docs/line-rendering-contract.md).
