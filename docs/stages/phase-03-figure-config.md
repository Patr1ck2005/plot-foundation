# Phase 3: Serializable Figure Configuration

Status: implementation complete on 2026-08-06; heatmap extension in progress

Release: `0.1.2`

`FigureConfig` is the next shared contract after the Phase 2 style policy. It
serializes figure geometry, axis limits/scales/aspect, a named style profile,
and an optional save-policy override. The object contains no output path,
directory creation, or Matplotlib figure, so it can safely live in a manifest
or task record.

Consumers should construct renderer input from `config.figure` and
`config.axes`, and use `config.resolved_save` with `save_figure()` at their
output boundary. This keeps output ownership in myPlots/Workbench while
making a figure reproducible from explicit data rather than process defaults.
