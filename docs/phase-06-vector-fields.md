# Phase 6: Vector And Director Fields

Release 0.1.5 adds a typed, domain-neutral vector field contract. Inputs use
the shared x-first orientation:

```text
u.shape == v.shape == (len(x), len(y))
```

`VectorFieldPlotSpec` makes sampling, arrow versus headless director glyphs,
optional color values, axes, figure geometry, and style explicit.
`render_vector_field` draws on caller-owned axes and does not save, close, show,
create directories, or write auxiliary mesh files.

The package does not interpret Stokes fields. A consumer may map `(S1,S2)` to
arrows or convert an orientation angle to `(cos(phi), sin(phi))` directors.

## Verification

- Non-square 3 x 5 fields preserve x/y/u/v/color orientation.
- Asymmetric sampling step `(2, 3)` selects the expected four glyphs.
- Zero-vector normalization is finite and remains zero.
- `phi` and `phi + pi` produce equivalent headless directors.
- Transposed fields are rejected instead of silently reoriented.
- Complete Plot Foundation suite: 19 passed under `MPLBACKEND=Agg`.
