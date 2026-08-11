# Phase 4: Heatmap Contract

Status: implementation complete on 2026-08-06

Release: `0.1.3`

`HeatmapPlotSpec` is the first two-dimensional renderer contract. It requires
`values.shape == (len(x), len(y))` and displays `values.T` on Cartesian axes,
matching the established myPlots orientation. `AxesSpec.aspect` is explicit:
`"equal"` preserves physical data units and `None`/`"auto"` allows the panel
to follow its figure geometry. Contours are optional and returned as artists;
colorbars are opt-in.

Physical normalization, symmetry completion, band selection, and schema
mapping remain in myPlots/Workbench adapters.
