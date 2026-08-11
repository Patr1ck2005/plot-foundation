from __future__ import annotations

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from plot_foundation import (
    AxesSpec,
    ColorMappedLineSeries,
    ColorMappedLineStyle,
    FigureSpec,
    FigureConfig,
    HeatmapPlotSpec,
    HeatmapStyle,
    LinePlotSpec,
    LineSeries,
    RibbonSeries,
    SeriesStyle,
    render_line_plot,
    plot_line_advanced,
    plot_2d_heatmap,
    render_heatmap,
)


def test_legacy_advanced_line_renderer_preserves_gradient_fill_contract():
    import matplotlib.pyplot as plt

    x = np.linspace(0.0, 1.0, 11)
    center = x**2
    width = np.full_like(x, 0.1)
    color = np.linspace(-1.0, 1.0, len(x))
    fig, ax = plt.subplots()

    result = plot_line_advanced(
        ax,
        x,
        center,
        z2=width,
        z3=color,
        enable_fill=True,
        gradient_fill=True,
        gradient_direction="z3",
        cmap="viridis",
    )

    assert result is ax
    assert len(ax.images) == 1
    assert len(ax.patches) == 1


def test_legacy_heatmap_renderer_preserves_x_first_imshow_contract():
    import matplotlib.pyplot as plt

    x = np.array([0.0, 1.0, 2.0])
    y = np.array([-1.0, 1.0])
    values = np.arange(6).reshape(3, 2) + 1j
    fig, ax = plt.subplots()
    returned_figure, returned_axes = plot_2d_heatmap(
        ax,
        x,
        y,
        values,
        {"cmap": "viridis", "imshow_aspect": "equal"},
    )

    assert returned_figure is fig
    assert returned_axes is ax
    np.testing.assert_array_equal(ax.images[0].get_array(), values.real.T)


def test_line_series_rejects_invalid_shape_and_complex_values():
    with pytest.raises(ValueError, match="lengths differ"):
        LineSeries([0, 1], [2])
    with pytest.raises(ValueError, match="real-valued"):
        LineSeries([0, 1], [1 + 1j, 2 + 0j])


def test_renderer_preserves_data_limits_when_guides_are_outside_range():
    spec = LinePlotSpec(
        series=(
            LineSeries([0, 1], [0.5, 0.6], label="data"),
            LineSeries(
                [0, 1],
                [5, 6],
                label="guide",
                role="guide",
                style=SeriesStyle(color="red", linestyle="--"),
            ),
        ),
        axes=AxesSpec(legend=True),
        preserve_data_y_limits=True,
    )
    result = render_line_plot(spec)
    assert len(result.artists) == 2
    assert result.axes.get_ylim()[1] < 1.0
    assert result.axes.get_legend_handles_labels()[1] == ["data", "guide"]


def test_renderer_supports_external_axes_scatter_and_log_scale():
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(figsize=(3, 2))
    spec = LinePlotSpec(
        series=(
            LineSeries(
                [0, 1, 2],
                [10, 100, 1000],
                label="Q",
                style=SeriesStyle(
                    kind="scatter", color="black", scatter_size=8, alpha=0.5
                ),
            ),
        ),
        axes=AxesSpec(xlabel="k", ylabel="Q", yscale="log", grid=True),
        figure=FigureSpec(figsize=(9, 9)),
    )
    result = render_line_plot(spec, ax=ax)
    assert result.figure is figure
    assert ax.get_yscale() == "log"
    np.testing.assert_allclose(result.artists[0].get_offsets()[:, 1], [10, 100, 1000])


def test_ribbon_uses_explicit_half_width_and_contributes_to_limits():
    x = np.linspace(0, 1, 5)
    center = np.full(5, 2.0)
    result = render_line_plot(
        LinePlotSpec(series=(RibbonSeries(x, center, np.full(5, 0.25)),))
    )
    assert result.axes.get_ylim()[0] < 1.75
    assert result.axes.get_ylim()[1] > 2.25


def test_colormapped_line_skips_nan_segments_and_autoscales():
    series = ColorMappedLineSeries(
        [0, 1, 2, 3],
        [10, 11, np.nan, 13],
        [0, 1, 2, 3],
        style=ColorMappedLineStyle(vmin=0, vmax=3, linewidth=2),
    )
    result = render_line_plot(LinePlotSpec(series=(series,)))
    assert len(result.artists[0].get_segments()) == 1
    assert result.axes.get_xlim()[1] >= 3


def test_figure_preset_and_aspect_are_explicit():
    spec = LinePlotSpec(
        series=(LineSeries([0, 1], [0, 1]),),
        axes=AxesSpec(aspect="equal"),
        figure=FigureSpec.from_preset("single"),
    )
    result = render_line_plot(spec)
    assert spec.figure.figsize == (1.5, 1.5)
    assert spec.figure.preset == "single"
    assert result.axes.get_aspect() == 1.0


def test_summary_preset_scales_panel_unit():
    spec = FigureSpec.from_preset("summary_panel", rows=2, cols=3)
    assert spec.figsize == (4.5, 3.0)


def test_figure_config_round_trips_geometry_axes_and_save_policy():
    config = FigureConfig(
        figure=FigureSpec.from_preset("single"),
        axes=AxesSpec(
            xlabel="k",
            xlim=(0.0, 1.0),
            ylim=(2.0, 3.0),
            aspect="equal",
        ),
        style_profile="preview",
    )
    restored = FigureConfig.from_dict(config.to_dict())
    assert restored == config
    assert restored.resolved_save.dpi == 150


def test_heatmap_transposes_xy_grid_and_applies_equal_aspect():
    x = [0.0, 1.0, 2.0]
    y = [-1.0, 1.0]
    values = [[0.0, 1.0], [2.0, 3.0], [4.0, 5.0]]
    result = render_heatmap(
        HeatmapPlotSpec(
            x,
            y,
            values,
            axes=AxesSpec(aspect="equal"),
            style=HeatmapStyle(contour_levels=(2.0, 4.0)),
        )
    )
    np.testing.assert_allclose(result.artists[0].get_array(), np.asarray(values).T)
    assert result.axes.get_aspect() == 1.0
    assert len(result.artists) == 2
