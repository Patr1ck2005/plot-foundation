# Phase 7: Multi-Surface Rendering

Release 0.1.6 separates multi-surface height, color, alpha, and explicit RGBA
channels. Every layer uses the x-first shape `(len(x), len(y))`; all layers
share one color normalization unless the caller supplies RGBA directly.

NaN height/color/alpha samples become transparent holes without rescaling the
physical z coordinate. The Matplotlib renderer has no filesystem side effects:
it never exports OBJ files, saves figures, creates directories, shows windows,
or closes caller-owned figures.

Consumers retain physical field names, colorbar labels, view policy, output
paths, and optional specialized backends such as myPlots' s3dlib smoothing.

## Verification

- Two non-square 3 x 5 layers with distinct physical z ranges.
- One NaN hole without normalization of z to 0..1.
- Global color limits shared across layers.
- Independent scalar/per-point alpha channels.
- Invalid RGBA and transposed height rejection.
- No `surface.obj` or other hidden output in the working directory.
- Complete package suite: 21 passed in both A and B environments under Agg.
