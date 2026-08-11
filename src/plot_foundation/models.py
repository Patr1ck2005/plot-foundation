"""Domain-neutral models for one-dimensional plots."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Sequence, TypeAlias

import numpy as np


SeriesKind = Literal["line", "scatter"]
SeriesRole = Literal["data", "guide"]
AxisScale = Literal["linear", "log", "symlog", "logit"]
AxisAspect = str | float | None


def _real_1d(values, *, name: str) -> np.ndarray:
    raw = np.asarray(values)
    if np.iscomplexobj(raw):
        raise ValueError(f"{name} must be real-valued")
    array = np.asarray(raw, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    return array.copy()


def _check_lengths(reference: np.ndarray, **arrays: np.ndarray) -> None:
    for name, array in arrays.items():
        if len(reference) != len(array):
            raise ValueError(
                f"plot series x/{name} lengths differ: "
                f"{len(reference)} != {len(array)}"
            )


@dataclass(frozen=True)
class SeriesStyle:
    """Backend-friendly style description for a plain line or scatter."""

    kind: SeriesKind = "line"
    color: Any | None = None
    linewidth: float | None = None
    linestyle: str = "-"
    marker: str | None = None
    marker_size: float = 4.0
    scatter_size: float = 8.0
    edge_color: Any | None = None
    alpha: float = 1.0
    zorder: float = 1.0

    def __post_init__(self) -> None:
        if self.kind not in {"line", "scatter"}:
            raise ValueError(f"unsupported series kind: {self.kind!r}")
        sizes = (self.marker_size, self.scatter_size)
        if self.linewidth is not None:
            sizes += (self.linewidth,)
        if any(value < 0 for value in sizes):
            raise ValueError("line, marker, and scatter sizes must be non-negative")
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")


@dataclass(frozen=True)
class RibbonStyle:
    """Style for a filled interval around a center line."""

    color: Any = "gray"
    alpha: float = 0.3
    edge_color: Any = "none"
    zorder: float = 0.0

    def __post_init__(self) -> None:
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")


@dataclass(frozen=True)
class ColorMappedLineStyle:
    """Style for a line whose segments are colored by a third array."""

    cmap: Any = "viridis"
    vmin: float | None = None
    vmax: float | None = None
    linewidth: float | None = None
    alpha: float = 1.0
    zorder: float = 2.0

    def __post_init__(self) -> None:
        if self.linewidth is not None and self.linewidth < 0:
            raise ValueError("linewidth must be non-negative")
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")
        if self.vmin is not None and self.vmax is not None and self.vmin > self.vmax:
            raise ValueError("vmin must not exceed vmax")


@dataclass(frozen=True)
class HeatmapStyle:
    """Color and optional contour policy for a scalar grid."""

    cmap: Any = "viridis"
    vmin: float | None = None
    vmax: float | None = None
    alpha: float = 1.0
    contour_levels: tuple[float, ...] | None = None
    contour_color: Any = "black"
    contour_linewidth: float = 0.5

    def __post_init__(self) -> None:
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")
        if self.vmin is not None and self.vmax is not None and self.vmin > self.vmax:
            raise ValueError("vmin must not exceed vmax")
        if self.contour_linewidth < 0:
            raise ValueError("contour_linewidth must be non-negative")


@dataclass(frozen=True)
class VectorFieldStyle:
    """Backend-neutral style for arrow or headless director fields."""

    color: Any | None = None
    cmap: Any = "viridis"
    vmin: float | None = None
    vmax: float | None = None
    normalize: bool = False
    scale: float | None = None
    pivot: str = "mid"
    width: float = 0.004
    alpha: float = 1.0

    def __post_init__(self) -> None:
        if self.vmin is not None and self.vmax is not None and self.vmin > self.vmax:
            raise ValueError("vmin must not exceed vmax")
        if self.width < 0:
            raise ValueError("width must be non-negative")
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")


@dataclass(frozen=True)
class SurfaceStyle:
    """Shared color, sampling, and shading policy for surface layers."""

    cmap: Any = "viridis"
    vmin: float | None = None
    vmax: float | None = None
    rstride: int = 1
    cstride: int = 1
    shade: bool = False

    def __post_init__(self) -> None:
        if self.vmin is not None and self.vmax is not None and self.vmin > self.vmax:
            raise ValueError("vmin must not exceed vmax")
        if self.rstride <= 0 or self.cstride <= 0:
            raise ValueError("surface strides must be positive")


@dataclass(frozen=True)
class SurfaceLayer:
    """Independent height, color, alpha, and optional RGBA surface channels."""

    z: Sequence[Sequence[float]] | np.ndarray
    color_values: Sequence[Sequence[float]] | np.ndarray | None = None
    alpha_values: Sequence[Sequence[float]] | np.ndarray | None = None
    rgba: np.ndarray | None = None
    alpha: float = 1.0
    alpha_vmin: float | None = None
    alpha_vmax: float | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.alpha <= 1:
            raise ValueError("surface alpha must be between 0 and 1")
        if self.alpha_vmin is not None and self.alpha_vmax is not None and self.alpha_vmin > self.alpha_vmax:
            raise ValueError("alpha_vmin must not exceed alpha_vmax")


@dataclass(frozen=True)
class LineSeries:
    """One real-valued line or scatter series."""

    x: Sequence[float] | np.ndarray
    y: Sequence[float] | np.ndarray
    label: str = ""
    role: SeriesRole = "data"
    style: SeriesStyle = field(default_factory=SeriesStyle)

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        y = _real_1d(self.y, name="y")
        _check_lengths(x, y=y)
        if self.role not in {"data", "guide"}:
            raise ValueError(f"unsupported series role: {self.role!r}")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)


@dataclass(frozen=True)
class RibbonSeries:
    """A filled interval described by center and non-negative half width."""

    x: Sequence[float] | np.ndarray
    center: Sequence[float] | np.ndarray
    half_width: Sequence[float] | np.ndarray
    label: str = ""
    role: SeriesRole = "data"
    style: RibbonStyle = field(default_factory=RibbonStyle)

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        center = _real_1d(self.center, name="center")
        half_width = _real_1d(self.half_width, name="half_width")
        _check_lengths(x, center=center, half_width=half_width)
        finite_width = half_width[np.isfinite(half_width)]
        if np.any(finite_width < 0):
            raise ValueError("half_width must be non-negative")
        if self.role not in {"data", "guide"}:
            raise ValueError(f"unsupported series role: {self.role!r}")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "center", center)
        object.__setattr__(self, "half_width", half_width)


@dataclass(frozen=True)
class ColorMappedLineSeries:
    """A line whose individual finite segments are colored by scalar values."""

    x: Sequence[float] | np.ndarray
    y: Sequence[float] | np.ndarray
    color_values: Sequence[float] | np.ndarray
    label: str = ""
    role: SeriesRole = "data"
    style: ColorMappedLineStyle = field(default_factory=ColorMappedLineStyle)

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        y = _real_1d(self.y, name="y")
        color_values = _real_1d(self.color_values, name="color_values")
        _check_lengths(x, y=y, color_values=color_values)
        if self.role not in {"data", "guide"}:
            raise ValueError(f"unsupported series role: {self.role!r}")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "color_values", color_values)


@dataclass(frozen=True)
class HeatmapPlotSpec:
    """Scalar grid with explicit x/y orientation and rendering policy.

    ``values`` is indexed as ``values[x_index, y_index]``. The Matplotlib
    renderer transposes it for Cartesian display using the x-first
    ``imshow(z.T, extent=...)`` convention.
    """

    x: Sequence[float] | np.ndarray
    y: Sequence[float] | np.ndarray
    values: Sequence[Sequence[float]] | np.ndarray
    axes: AxesSpec = field(default_factory=lambda: AxesSpec())
    figure: FigureSpec = field(default_factory=lambda: FigureSpec())
    style: HeatmapStyle = field(default_factory=HeatmapStyle)
    colorbar: bool = False
    colorbar_label: str = ""

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        y = _real_1d(self.y, name="y")
        values = np.asarray(self.values)
        if np.iscomplexobj(values):
            raise ValueError("values must be real-valued")
        values = np.asarray(values, dtype=float)
        expected = (len(x), len(y))
        if values.ndim != 2 or values.shape != expected:
            raise ValueError(
                f"values must have shape (len(x), len(y))={expected}, got {values.shape}"
            )
        object.__setattr__(self, "x", x.copy())
        object.__setattr__(self, "y", y.copy())
        object.__setattr__(self, "values", values.copy())


PlotSeries: TypeAlias = LineSeries | RibbonSeries | ColorMappedLineSeries


@dataclass(frozen=True)
class AxesSpec:
    """Labels, scales, limits, grid, and legend policy."""

    xlabel: str = ""
    ylabel: str = ""
    title: str = ""
    xscale: AxisScale = "linear"
    yscale: AxisScale = "linear"
    xlim: tuple[float, float] | None = None
    ylim: tuple[float, float] | None = None
    aspect: AxisAspect = None
    grid: bool = False
    grid_alpha: float = 0.3
    legend: bool = False
    legend_loc: str = "best"
    legend_ncol: int = 1
    legend_fontsize: float | None = None

    def __post_init__(self) -> None:
        valid_scales = {"linear", "log", "symlog", "logit"}
        if self.xscale not in valid_scales or self.yscale not in valid_scales:
            raise ValueError("unsupported axis scale")
        if self.legend_ncol <= 0:
            raise ValueError("legend_ncol must be positive")
        if not 0 <= self.grid_alpha <= 1:
            raise ValueError("grid_alpha must be between 0 and 1")

    def to_dict(self) -> dict:
        return {
            "xlabel": self.xlabel,
            "ylabel": self.ylabel,
            "title": self.title,
            "xscale": self.xscale,
            "yscale": self.yscale,
            "xlim": list(self.xlim) if self.xlim is not None else None,
            "ylim": list(self.ylim) if self.ylim is not None else None,
            "aspect": self.aspect,
            "grid": self.grid,
            "grid_alpha": self.grid_alpha,
            "legend": self.legend,
            "legend_loc": self.legend_loc,
            "legend_ncol": self.legend_ncol,
            "legend_fontsize": self.legend_fontsize,
        }

    @classmethod
    def from_dict(cls, values: dict) -> "AxesSpec":
        data = dict(values)
        for key in ("xlim", "ylim"):
            if data.get(key) is not None:
                data[key] = tuple(data[key])
        return cls(**data)


@dataclass(frozen=True)
class FigureSpec:
    """Figure creation and final layout settings."""

    figsize: tuple[float, float] = (6.0, 4.0)
    tight_layout: bool = False
    preset: str | None = None

    def __post_init__(self) -> None:
        if len(self.figsize) != 2 or any(value <= 0 for value in self.figsize):
            raise ValueError("figsize must contain two positive values")

    def to_dict(self) -> dict:
        return {
            "figsize": list(self.figsize),
            "tight_layout": self.tight_layout,
            "preset": self.preset,
        }

    @classmethod
    def from_dict(cls, values: dict) -> "FigureSpec":
        data = dict(values)
        if "figsize" in data:
            data["figsize"] = tuple(data["figsize"])
        return cls(**data)

    @classmethod
    def from_preset(cls, name: str, *, rows: int = 1, cols: int = 1, **overrides):
        """Create a figure spec from a named policy preset.

        ``rows`` and ``cols`` only affect the ``summary_panel`` preset. Any
        explicit override wins over the preset value.
        """

        from .style import figure_preset

        preset = figure_preset(name, rows=rows, cols=cols)
        values = {
            "figsize": preset.figsize,
            "tight_layout": False,
            "preset": name,
        }
        values.update(overrides)
        return cls(**values)


@dataclass(frozen=True)
class VectorFieldPlotSpec:
    """Explicit x-first vector field sampled onto arrows or directors."""

    x: Sequence[float] | np.ndarray
    y: Sequence[float] | np.ndarray
    u: Sequence[Sequence[float]] | np.ndarray
    v: Sequence[Sequence[float]] | np.ndarray
    color_values: Sequence[Sequence[float]] | np.ndarray | None = None
    glyph: Literal["arrow", "director"] = "arrow"
    step: tuple[int, int] = (1, 1)
    axes: AxesSpec = field(default_factory=lambda: AxesSpec(aspect="equal"))
    figure: FigureSpec = field(default_factory=FigureSpec)
    style: VectorFieldStyle = field(default_factory=VectorFieldStyle)

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        y = _real_1d(self.y, name="y")
        expected = (len(x), len(y))
        fields = []
        for name, values in (("u", self.u), ("v", self.v)):
            values = np.asarray(values)
            if np.iscomplexobj(values):
                raise ValueError(f"{name} must be real-valued")
            values = np.asarray(values, dtype=float)
            if values.shape != expected:
                raise ValueError(f"{name} must have x-first shape {expected}")
            fields.append(values.copy())
        colors = None
        if self.color_values is not None:
            colors = np.asarray(self.color_values, dtype=float)
            if colors.shape != expected:
                raise ValueError(f"color_values must have x-first shape {expected}")
            colors = colors.copy()
        if self.glyph not in {"arrow", "director"}:
            raise ValueError("glyph must be 'arrow' or 'director'")
        if len(self.step) != 2 or any(int(value) <= 0 for value in self.step):
            raise ValueError("step must contain two positive integers")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "u", fields[0])
        object.__setattr__(self, "v", fields[1])
        object.__setattr__(self, "color_values", colors)
        object.__setattr__(self, "step", tuple(int(value) for value in self.step))


@dataclass(frozen=True)
class MultiSurfacePlotSpec:
    """Multiple x-first surface layers sharing one color normalization."""

    x: Sequence[float] | np.ndarray
    y: Sequence[float] | np.ndarray
    layers: tuple[SurfaceLayer, ...] | Sequence[SurfaceLayer]
    figure: FigureSpec = field(default_factory=FigureSpec)
    style: SurfaceStyle = field(default_factory=SurfaceStyle)
    xlabel: str = ""
    ylabel: str = ""
    zlabel: str = ""
    elev: float = 30.0
    azim: float = 25.0
    box_aspect: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        x = _real_1d(self.x, name="x")
        y = _real_1d(self.y, name="y")
        layers = tuple(self.layers)
        if not layers:
            raise ValueError("surface layers cannot be empty")
        expected = (len(x), len(y))
        checked = []
        for layer in layers:
            z = np.asarray(layer.z, dtype=float)
            if z.shape != expected:
                raise ValueError(f"surface z must have x-first shape {expected}")
            values = {}
            for name in ("color_values", "alpha_values"):
                field_values = getattr(layer, name)
                if field_values is not None:
                    field_values = np.asarray(field_values, dtype=float)
                    if field_values.shape != expected:
                        raise ValueError(f"surface {name} must have x-first shape {expected}")
                    values[name] = field_values.copy()
            rgba = None
            if layer.rgba is not None:
                rgba = np.asarray(layer.rgba, dtype=float)
                if rgba.shape != (*expected, 4):
                    raise ValueError(f"surface rgba must have shape {(*expected, 4)}")
                rgba = rgba.copy()
            checked.append(
                SurfaceLayer(
                    z=z.copy(),
                    color_values=values.get("color_values"),
                    alpha_values=values.get("alpha_values"),
                    rgba=rgba,
                    alpha=layer.alpha,
                    alpha_vmin=layer.alpha_vmin,
                    alpha_vmax=layer.alpha_vmax,
                )
            )
        if len(self.box_aspect) != 3 or any(value <= 0 for value in self.box_aspect):
            raise ValueError("box_aspect must contain three positive values")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "layers", tuple(checked))


@dataclass(frozen=True)
class LinePlotSpec:
    """Complete renderer input independent of schemas and file paths."""

    series: tuple[PlotSeries, ...] | Sequence[PlotSeries]
    axes: AxesSpec = field(default_factory=AxesSpec)
    figure: FigureSpec = field(default_factory=FigureSpec)
    preserve_data_y_limits: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "series", tuple(self.series))
