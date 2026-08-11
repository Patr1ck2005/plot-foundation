# Phase 2: Style and Figure Policy

Status: implementation complete, verification in progress

Date: 2026-08-06

## Purpose

Phase 2 makes the plotting conventions learned in myPlots explicit and
portable without forcing those publication conventions onto operational
Workbench figures. The policy is configuration, not hidden Matplotlib global
state.

## Portable contract

- `MatplotlibStyle` provides a scoped font and axis policy: 9 pt text,
  Arial with `DejaVu Sans` fallback, inward x/y ticks, no grid by default,
  and 1 pt default lines.
- `style_context()` restores every modified `rcParams` value on exit.
- `FigureSpec.from_preset()` provides semantic geometry:
  `single=(1.5, 1.5)`, `summary_panel=1.5` inches per panel,
  `overview_3d=(2.0, 2.0)`, and `line=(4.0, 3.0)`.
- `AxesSpec.aspect` is explicit and is applied after data and guide artists
  are created. Heatmap and image consumers must set it deliberately.
- `SaveSpec.paper()` uses transparent PNG output, 300 DPI, and
  `bbox_inches="tight"`; `SaveSpec.preview()` is identical at 150 DPI.
- Renderers do not call `show()`, `savefig()`, `close()`, create directories,
  or invoke `tight_layout()` unless the figure spec explicitly opts in.

## Consumer boundaries

myPlots keeps ownership of Chinese schemas, physical interpretation,
publication labels, batch layout, and legacy figure sizes. Its shared adapter
derives a scoped style from `PlotConfig`, so existing calls retain their
behavior and global Matplotlib state is unchanged.

ResearchAgentWorkbench keeps its operational compatibility profile: frequency
figures `(10, 6)`, Q figures `(10, 5)`, two-panel overviews `(10, 10)`, and
150 DPI. This is intentionally distinct from the paper profile; a future
paper-output workflow can select `PAPER_PROFILE` without changing operational
artifacts.

## Verification gate

The phase is complete when the source-tree and installed-wheel test suites
pass in both analysis environments, the A shared/legacy image contract is
unchanged, and the B acceptance sidecar records Plot Foundation `0.1.1` with
`install_mode="wheel"`. New consumers must serialize figure geometry, axis
limits, aspect, DPI, and selected style profile rather than relying on
process-global defaults.
