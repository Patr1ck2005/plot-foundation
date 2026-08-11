from __future__ import annotations

import matplotlib
import numpy as np

matplotlib.use("Agg")

from plot_foundation import (
    add_annotations,
    draw_shapes,
    extract_contour_paths,
    plot_1d_lines,
    plot_2d_multiline,
    plot_iso_contours2D,
    plot_paths,
    plot_scatter_advanced,
    imshow_phi,
    imshow_s3,
    plot_polar_line,
)


def test_advanced_scatter_preserves_size_color_and_axes_contract():
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots()
    result = plot_scatter_advanced(
        ax,
        np.array([0.0, 1.0, 2.0]),
        np.array([1.0, 2.0, 3.0]),
        z2=np.array([1.0, 2.0, 3.0]),
        z3=np.array([-1.0, 0.0, 1.0]),
        enable_size_variation=True,
        enable_dynamic_color=True,
        s_base=10,
        scale=2,
    )
    assert result is ax
    np.testing.assert_array_equal(ax.collections[0].get_sizes(), [12, 14, 16])
    plt.close(figure)


def test_contour_extraction_and_rendering_are_x_first_and_headless():
    import matplotlib.pyplot as plt

    x = np.linspace(-1.0, 1.0, 9)
    y = np.linspace(-2.0, 2.0, 13)
    values = x[:, None] ** 2 + y[None, :] ** 2
    before = set(plt.get_fignums())
    paths = extract_contour_paths(x, y, values, 1.0)
    assert paths
    assert set(plt.get_fignums()) == before
    figure, ax = plt.subplots()
    assert plot_iso_contours2D(ax, x, y, values, [1.0]) is ax
    artists = plot_paths(ax, paths[:1], colors="black")
    assert len(artists) == 1
    plt.close(figure)


def test_multiline_renderers_preserve_return_and_artist_contracts():
    import matplotlib.pyplot as plt

    x = np.array([0.0, 1.0, 2.0])
    figure, ax = plt.subplots()
    returned, returned_ax = plot_1d_lines(ax, x, [x + 1j * 0.1], {"enable_line_fill": False})
    assert returned is figure and returned_ax is ax
    assert len(ax.lines) == 1
    plt.close(figure)

    figure, ax = plt.subplots()
    y = np.array([0.0, 1.0])
    values = np.column_stack((x, x + 1.0)).astype(complex)
    returned, returned_ax = plot_2d_multiline(ax, x, y, values, {})
    assert returned is figure and returned_ax is ax
    assert len(ax.lines) == 2
    plt.close(figure)


def test_basic_shape_and_annotation_helpers_preserve_axes_contract():
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots()
    assert draw_shapes(ax, [0, 1], [1, 2], label="data") is ax
    assert add_annotations(
        ax,
        xlabel="x",
        ylabel="y",
        show_legend=True,
        xtick_mode="manual",
        xticks=[0, 1],
    ) is ax
    assert ax.get_xlabel() == "x"
    assert ax.get_legend() is not None
    plt.close(figure)


def test_polar_and_scalar_map_helpers_preserve_historical_artists():
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(subplot_kw={"projection": "polar"})
    assert plot_polar_line(ax, np.array([0.0, 90.0]), np.array([1.0, 2.0])) is ax
    assert len(ax.lines) == 1
    plt.close(figure)

    figure, axes = plt.subplots(1, 2)
    field = np.arange(6).reshape(3, 2)
    assert imshow_phi(axes[0], field, cmap="twilight") is axes[0]
    assert imshow_s3(axes[1], field, cmap="RdBu") is axes[1]
    np.testing.assert_array_equal(axes[0].images[0].get_array(), field.T)
    plt.close(figure)
