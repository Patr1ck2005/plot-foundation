from __future__ import annotations

import numpy as np
import pytest

from plot_foundation import (
    MultiSurfacePlotSpec,
    SurfaceLayer,
    SurfaceStyle,
    render_multi_surface_3d,
)


def test_non_square_layers_keep_physical_height_global_color_and_nan_holes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    x = np.asarray([-2.0, 0.0, 3.0])
    y = np.asarray([-4.0, -1.0, 0.0, 2.0, 5.0])
    X, Y = np.meshgrid(x, y, indexing="ij")
    z1 = 10.0 + X + 0.2 * Y
    z2 = 30.0 + 2 * X - 0.1 * Y
    z2[1, 2] = np.nan
    result = render_multi_surface_3d(
        MultiSurfacePlotSpec(
            x=x,
            y=y,
            layers=(
                SurfaceLayer(z1, color_values=X - Y, alpha=0.7),
                SurfaceLayer(z2, color_values=2 * X + Y, alpha_values=np.abs(X - Y)),
            ),
            style=SurfaceStyle(cmap="viridis"),
        )
    )
    assert len(result.artists) == 2
    assert result.axes.get_zlim()[1] > 20.0
    assert result.artists[0].get_clim() == result.artists[1].get_clim()
    assert list(tmp_path.iterdir()) == []


def test_explicit_rgba_shape_and_transposed_height_are_rejected():
    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 1, 5)
    z = np.zeros((3, 5))
    with pytest.raises(ValueError, match="rgba"):
        MultiSurfacePlotSpec(x=x, y=y, layers=(SurfaceLayer(z, rgba=np.zeros((5, 3, 4))),))
    with pytest.raises(ValueError, match="x-first"):
        MultiSurfacePlotSpec(x=x, y=y, layers=(SurfaceLayer(z.T),))


def test_nan_color_holes_survive_draw_without_array_override():
    """set_array() must NOT be set on the collection: it forces draw-time
    facecolor recomputation, turning NaN holes into the cmap bad color
    (regression: uniform/noise surfaces) and exploding SVG export memory
    on dense grids."""
    import matplotlib

    matplotlib.use("Agg")
    x = np.linspace(0.0, 1.0, 6)
    y = np.linspace(0.0, 1.0, 6)
    X, Y = np.meshgrid(x, y, indexing="ij")
    z = X + Y
    color = X - Y
    color[2, 2] = np.nan  # hole
    result = render_multi_surface_3d(
        MultiSurfacePlotSpec(
            x=x, y=y, layers=(SurfaceLayer(z, color_values=color),),
            style=SurfaceStyle(cmap="viridis"),
        )
    )
    artist = result.artists[0]
    assert artist.get_array() is None  # no draw-time recolor channel
    face_alpha = np.asarray(artist._facecolor3d)[:, 3]
    assert np.any(face_alpha == 0.0)  # the NaN hole stays a transparent quad
    assert np.any(face_alpha > 0.0)  # finite cells stay opaque
    result.figure.canvas.draw()  # must not raise or recolor
