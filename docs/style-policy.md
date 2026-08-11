# Style Policy and myPlots Experience Audit

This policy separates portable rendering knowledge from consumer-specific
publication and physics rules.

## Promoted into Plot Foundation

- Typed style and figure specifications rather than unvalidated dictionaries.
- `tight_layout` is opt-in and disabled by default.
- Grid is disabled by default.
- Default line width is controlled by a scoped style profile; a series only
  overrides it explicitly when the visual contract requires it.
- Font size 9, inward ticks, and Arial with DejaVu Sans fallback are available
  through `style_context()` without permanently mutating global `rcParams`.
- Saving is explicit, transparent by default, uses tight output cropping, and
  never creates directories. Output cropping is not layout mutation.
- Renderers return artists and never call `show`, `savefig`, or `close`.
- Filled intervals and color-mapped lines are first-class primitives. NaNs
  create real visual gaps instead of accidental cross-gap segments.
- Presentation policy is explicit. `publication_minimal` suppresses titles,
  axis labels, legends, colorbars, grids, and automatic layout mutation;
  `diagnostic` retains those aids for analysis figures. Physical choices such
  as aspect, limits, normalization, and colormap remain caller-owned.

The current semantic figure presets are:

| Preset | Default geometry | Intended use |
| --- | --- | --- |
| `single` | `(1.5, 1.5)` | paper-level single panel |
| `summary_panel` | `1.5` inch per row/column panel | paper summary grids |
| `overview_3d` | `(2.0, 2.0)` | compact 3D overview |
| `line` | `(4.0, 3.0)` | general line renderer fallback |

`PUBLICATION_MINIMAL_PROFILE` and its backwards-compatible `PAPER_PROFILE`
alias use 300 DPI. `PREVIEW_PROFILE` uses the same minimal presentation at
150 DPI. `DIAGNOSTIC_PROFILE` uses 150 DPI and enables diagnostic chrome.
Use `profile_context()` to scope Matplotlib settings and `profile()` to resolve
configuration names. Profiles are inputs, not hidden global state; a consumer
may override dimensions, DPI, or axis limits per figure.

`FigureConfig` serializes those per-figure choices (geometry, limits, scales,
aspect, profile name, and optional save override) without including paths or
Matplotlib objects. Use it at manifest/task boundaries when a figure must be
reproduced later.

## Kept in myPlots

- Chinese DataFrame columns, TSV/object-grid ingestion, Visualizer lifecycle,
  and project batch composition.
- The physical rule that a frequency ribbon has total width
  `2 * abs(imaginary_frequency)`. Plot Foundation only knows an explicit half
  width; the adapter owns that interpretation.
- Diffraction, band tracking, symmetry completion, polarization, and Poincare
  semantics.
- Per-project figure sizes, axis ranges, target bands, output hierarchies, and
  run manifests.

## Deferred candidates

Heatmap/contour, multi-surface, polar, ellipse, Poincare, SVG composition, and
batch layout need separate characterization phases. Existing myPlots functions
mix generic rendering with orientation, physical normalization, output, or
workflow policy; moving them without first splitting those concerns would make
this package less general.
