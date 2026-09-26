# Style Policy and myPlots Experience Audit

This policy separates portable rendering knowledge from consumer-specific
publication and physics rules.

## Promoted into Plot Foundation

- Typed style and figure specifications rather than unvalidated dictionaries.
- `tight_layout` is opt-in and disabled by default.
- Grid is disabled by default.
- Default line width is controlled by a scoped style profile; a series only
  overrides it explicitly when the visual contract requires it.
- The compatibility `MatplotlibStyle` default is still 9 pt, with inward ticks
  and Arial/DejaVu Sans. The current user delivery requirement below is 8 pt;
  select it explicitly through the supported scoped style configuration.
  This document update does not change installed library defaults or old figures.
- Saving is explicit, transparent by default, and never creates directories.
  The default is tight output cropping. Fixed physical-size delivery must
  explicitly use `SaveSpec(bbox_inches=None)`; cropping changes exported page
  dimensions even though it does not change the axes layout.
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

<a id="a4-paper-delivery"></a>
## A4 portrait / PowerPoint delivery (user clarification, 2026-09-21)

**Updated by explicit user clarification, 2026-09-26:** new scientific figures
use 8 pt text and inward ticks. Preserve historical figures. The baseline
deliverable is compact, reusable individual panels that the user can insert
at their declared physical size and freely assemble in PowerPoint on an A4
page. Selection/composition, a complete paper figure package, and a manuscript
draft are separate optional scopes. Exploration does not automatically require
any of them. This clarification retains the new typography and corrects the
earlier same-day wording that made a complete figure package the default.

Physical size is part of the output contract, not a cosmetic afterthought.
Discrete panels must remain suitable for user assembly on an A4 portrait page
in PowerPoint or another editor. The user may assemble them personally or
delegate selection and composition. Required visual standards do not determine
how far the research or writing task must go.

### Font size and column budget

- Use **8 pt** as the base size for all visible text: axes, tick labels,
  legends, colorbar ticks, annotations, and panel letters. Use the shared Arial
  style. Mathematical subscripts follow normal mathematical typesetting.
  Explicit artist-level font settings must match the intended final size.
- Ticks point inward: `xtick.direction = ytick.direction = 'in'`, or the
  equivalent `tick_params(direction='in')`. Keep tick marks even when compact
  reusable panels omit redundant numeric labels.
- A4 is **210 × 297 mm**. Per the user's explicit calibration, use half of
  the full page width for one column: **105 mm = 4.13386 in**, and the full
  page width for two columns: **210 mm = 8.26772 in**. Do not deduct page
  margins or a column gutter from these widths. These are the user's figure
  calibration widths, not a publisher specification.
- A **2 × 2 arrangement normally fits one column**. Larger arrangements may
  use two columns. Choose the column budget first, then divide it among panels,
  gutters, axes, legends, and colorbars. Do not assign a whole column's width
  to each member of a 2 × 2 arrangement.
- Typical 2D panel canvases are **1 × 1, 1.25 × 1.25, or 1.5 × 1.5 in**.
  A non-square panel may be declared when its content requires it. The existing
  `single=(1.5, 1.5)` preset is a useful upper starting point for ordinary
  compact panels; `line=(4, 3)` is a renderer fallback, not a publication default.
- A simple row budget is `sum(panel widths) + gutters + outer annotation
  space <= target column width`. For example, two 1.25 in panels consume
  63.5 mm, leaving 41.5 mm within the 105 mm calibration width for axes,
  annotations, and spacing between panels. Such internal spacing does not
  reduce the declared single-column or two-column width.
- Height follows content and the available A4 page area; single-column does
  not imply a square final figure. Keep font size at 8 pt when fitting content.

### Rich panel collection and optional composition

- For ordinary exploration, deliver individual PNG/SVG panels and retain their
  generation code and source mapping. Use the existing manifest or configuration
  for `figsize`, exported physical width/height, DPI, profile and intended
  placement size; shared settings can be recorded once per figure family with
  per-panel exceptions. A new reporting document per image is not required.
- A research task may systematically generate many useful figures covering
  parameter space, mechanisms, controls, failure cases and validity limits.
  Hundreds of panels may be useful; compact `figsize` is not a limit on figure
  count or a quota to fill. Keep the full useful collection even when only a
  small selection is presented. Exploration can be organized by scientific
  argument without being packaged as a complete paper.
- When selection/composition is requested, choose informative panels, explain
  the selection briefly, and assemble logical groups. Choose single-column or
  double-column layouts as useful; both variants are not required by default.
  Keep the independent panels and editable composite sources for user assembly.
- Only for an explicitly requested complete-paper figure task, develop the
  full figure story, create useful concept diagrams (such as Fig. 1), and
  organize main-text and supplementary figures with captions and evidence
  gaps. A manuscript draft requires a writing task. A proposed story or layout
  is not final scientific acceptance. Reusable task wording is maintained in
  [MyPhysics F1/F2/F3 and W modules](D:/Obsidian/MyPhysics/Resources/Prompts/Recipes/科研研究.md).
- Concept diagrams must distinguish illustration from simulated evidence and
  accurately represent geometry, excitation, observables and mechanisms.
  Preserve editable/vector elements where suitable. Each scientific figure
  must remain traceable to its input data, processing and generation code.
- With the minimal publication profile, retain tick marks and suppress numeric
  tick labels where needed. Do not remove all ticks to solve crowding. Move
  legends/colorbars to separate assets or simplify annotations before enlarging
  panels or reducing the 8 pt font. The assembled figure must restore sufficient
  axes, units, color scales and labels to be scientifically interpretable;
  shared annotations can serve multiple panels. The minimal profile is not
  permission to remove necessary meaning from a final figure. When delivering
  panels for user assembly, preserve the missing shared labels/color scales as
  reusable assets or in their source configuration; do not require an agent-made
  composite merely to complete the basic panel delivery.
- Any enlarged diagnostic view must be explicitly identified as such, never
  the default asset handed over for direct PowerPoint insertion.

### Preserve size through export and insertion

`figsize` is the canvas size **in inches**, not just the axes rectangle. Set
axes margins inside this canvas. Use the existing fixed-canvas save override:

```python
from dataclasses import replace
from plot_foundation import profile, profile_context, save_figure

selected = profile("publication_minimal")
selected = replace(
    selected,
    style=replace(selected.style, font_size=8.0,
                  xtick_direction="in", ytick_direction="in"),
)
fixed_canvas = replace(selected.save, bbox_inches=None)
with profile_context(selected):
    # Caller creates the figure, applies presentation policy, and places axes.
    # The destination's parent directory is also caller-owned.
    save_figure(figure, path, fixed_canvas)
```

Do not rely on `bbox_inches="tight"` for an exact-size PowerPoint asset: it may
shrink or expand the exported SVG/PDF/PNG relative to the declared `figsize`.
Do not render large and scale the finished image down to the target width:
the nominal 8 pt lettering would shrink with the image. Re-render at the
intended physical size with the same shared font policy.

Verify the exported SVG width/height or PDF page box, and the PNG pixel size
plus DPI metadata. A 1.25 in square is 90 × 90 pt in SVG/PDF and 375 × 375 px
at 300 DPI. Allow at most one raster pixel for rounding. Record intended
insertion sizes in cm/mm for PowerPoint; if insertion or clipboard handling
changes the size, restore those dimensions rather than visually resizing it.

The fixed-canvas choice is an explicit per-output override. It does not change
the library's backwards-compatible tight-crop default or require a new preset.
Likewise, the typography override uses existing APIs; selecting a profile name
alone still uses its compatibility font default. Workbench callers can use
`figure_style("publication_minimal", font_size=8.0)`. Validate the delivered
panels, and composites when requested, at their intended physical size,
including text, ticks, exported dimensions, readability and physical meaning.

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

## Historical deferred candidates

The following records the early extraction audit, not the current capability
list. Use the repository README and public API for implemented features.

Heatmap/contour, multi-surface, polar, ellipse, Poincare, SVG composition, and
batch layout need separate characterization phases. Existing myPlots functions
mix generic rendering with orientation, physical normalization, output, or
workflow policy; moving them without first splitting those concerns would make
this package less general.
