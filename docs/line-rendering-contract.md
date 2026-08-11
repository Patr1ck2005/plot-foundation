# Line Rendering Contract

The renderer accepts real one-dimensional arrays through typed series:

- `LineSeries`: ordinary line or scatter.
- `RibbonSeries`: center plus an explicitly non-negative half width.
- `ColorMappedLineSeries`: finite line segments colored by a scalar array.

Every series has a `data` or `guide` role. Data is drawn first. When
`preserve_data_y_limits=True`, guide lines cannot expand the data-derived
y-limits. This supports reference thresholds without changing the visible data
window.

NaN values remain gaps. The color-mapped renderer discards any segment whose
two endpoints or color values are not finite; it never connects across a gap.
Renderers do not save, close, create directories, or mutate global style. A
consumer may set `AxesSpec.aspect` explicitly; `FigureSpec.from_preset()` keeps
geometry decisions visible and serializable rather than hiding them in a
renderer.
