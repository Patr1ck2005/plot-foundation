"""Matplotlib renderer for domain-neutral line plot specifications."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .models import (
    ColorMappedLineSeries,
    HeatmapPlotSpec,
    LinePlotSpec,
    LineSeries,
    MultiSurfacePlotSpec,
    RibbonSeries,
    VectorFieldPlotSpec,
)


@dataclass(frozen=True)
class RenderResult:
    """Figure, axes, and artists produced by one render call."""

    figure: Any
    axes: Any
    artists: tuple[Any, ...]


def _draw_plain(ax, series: LineSeries):
    style = series.style
    common = {"alpha": style.alpha, "label": series.label, "zorder": style.zorder}
    if style.color is not None:
        common["color"] = style.color
    if style.kind == "scatter":
        common["s"] = style.scatter_size
        if style.marker is not None:
            common["marker"] = style.marker
        if style.edge_color is not None:
            common["edgecolors"] = style.edge_color
        return ax.scatter(series.x, series.y, **common)
    common.update(
        {
            "linestyle": style.linestyle,
            "marker": style.marker,
            "markersize": style.marker_size,
        }
    )
    if style.linewidth is not None:
        common["linewidth"] = style.linewidth
    return ax.plot(series.x, series.y, **common)[0]


def _draw_ribbon(ax, series: RibbonSeries):
    lower = series.center - series.half_width
    upper = series.center + series.half_width
    return ax.fill_between(
        series.x,
        lower,
        upper,
        color=series.style.color,
        alpha=series.style.alpha,
        edgecolor=series.style.edge_color,
        label=series.label,
        zorder=series.style.zorder,
    )


def _draw_colormapped(ax, series: ColorMappedLineSeries):
    from matplotlib.collections import LineCollection
    from matplotlib.colors import Normalize

    points = np.column_stack((series.x, series.y))
    finite = np.isfinite(series.x) & np.isfinite(series.y) & np.isfinite(
        series.color_values
    )
    segment_mask = finite[:-1] & finite[1:]
    segments = np.stack((points[:-1], points[1:]), axis=1)[segment_mask]
    colors = ((series.color_values[:-1] + series.color_values[1:]) / 2)[segment_mask]
    finite_colors = series.color_values[np.isfinite(series.color_values)]
    vmin = series.style.vmin
    vmax = series.style.vmax
    if finite_colors.size:
        if vmin is None:
            vmin = float(np.min(finite_colors))
        if vmax is None:
            vmax = float(np.max(finite_colors))
    if vmin is None:
        vmin = 0.0
    if vmax is None:
        vmax = 1.0
    if vmax == vmin:
        vmax = vmin + 1.0
    options = {
        "array": colors,
        "cmap": series.style.cmap,
        "norm": Normalize(vmin=vmin, vmax=vmax),
        "alpha": series.style.alpha,
        "label": series.label,
        "zorder": series.style.zorder,
    }
    if series.style.linewidth is not None:
        options["linewidth"] = series.style.linewidth
    collection = LineCollection(segments, **options)
    ax.add_collection(collection)
    if np.any(finite):
        ax.update_datalim(points[finite])
        ax.autoscale_view()
    return collection


def _draw_series(ax, series):
    if isinstance(series, RibbonSeries):
        return _draw_ribbon(ax, series)
    if isinstance(series, ColorMappedLineSeries):
        return _draw_colormapped(ax, series)
    if isinstance(series, LineSeries):
        return _draw_plain(ax, series)
    raise TypeError(f"unsupported series type: {type(series).__name__}")


def render_line_plot(spec: LinePlotSpec, *, ax=None) -> RenderResult:
    """Render without creating directories, saving, closing, or global styling."""

    import matplotlib.pyplot as plt

    if ax is None:
        figure, ax = plt.subplots(figsize=spec.figure.figsize)
    else:
        figure = ax.figure

    artists = []
    for series in spec.series:
        if series.role == "data":
            artists.append(_draw_series(ax, series))

    axes_spec = spec.axes
    ax.set_xscale(axes_spec.xscale)
    ax.set_yscale(axes_spec.yscale)
    data_ylim = ax.get_ylim()

    for series in spec.series:
        if series.role == "guide":
            artists.append(_draw_series(ax, series))

    ax.set_xlabel(axes_spec.xlabel)
    ax.set_ylabel(axes_spec.ylabel)
    ax.set_title(axes_spec.title)
    if axes_spec.xlim is not None:
        ax.set_xlim(axes_spec.xlim)
    if axes_spec.ylim is not None:
        ax.set_ylim(axes_spec.ylim)
    elif spec.preserve_data_y_limits:
        ax.set_ylim(data_ylim)
    if axes_spec.aspect is not None:
        ax.set_aspect(axes_spec.aspect, adjustable="box")
    if axes_spec.grid:
        ax.grid(True, alpha=axes_spec.grid_alpha)
    if axes_spec.legend and ax.get_legend_handles_labels()[0]:
        legend_options = {
            "loc": axes_spec.legend_loc,
            "ncol": axes_spec.legend_ncol,
        }
        if axes_spec.legend_fontsize is not None:
            legend_options["fontsize"] = axes_spec.legend_fontsize
        ax.legend(**legend_options)
    if spec.figure.tight_layout:
        figure.tight_layout()
    return RenderResult(figure=figure, axes=ax, artists=tuple(artists))


def render_heatmap(spec: HeatmapPlotSpec, *, ax=None) -> RenderResult:
    """Render a scalar grid without saving, closing, or creating directories."""

    import matplotlib.pyplot as plt

    if ax is None:
        figure, ax = plt.subplots(figsize=spec.figure.figsize)
    else:
        figure = ax.figure

    x = np.asarray(spec.x)
    y = np.asarray(spec.y)
    values = np.asarray(spec.values)
    X, Y = np.meshgrid(x, y, indexing="xy")
    options = {
        "cmap": spec.style.cmap,
        "vmin": spec.style.vmin,
        "vmax": spec.style.vmax,
        "shading": "auto",
        "alpha": spec.style.alpha,
    }
    mappable = ax.pcolormesh(X, Y, values.T, **options)
    artists = [mappable]
    if spec.style.contour_levels is not None:
        contours = ax.contour(
            X,
            Y,
            values.T,
            levels=spec.style.contour_levels,
            colors=spec.style.contour_color,
            linewidths=spec.style.contour_linewidth,
        )
        artists.append(contours)

    axes_spec = spec.axes
    ax.set_xscale(axes_spec.xscale)
    ax.set_yscale(axes_spec.yscale)
    ax.set_xlabel(axes_spec.xlabel)
    ax.set_ylabel(axes_spec.ylabel)
    ax.set_title(axes_spec.title)
    if axes_spec.xlim is not None:
        ax.set_xlim(axes_spec.xlim)
    if axes_spec.ylim is not None:
        ax.set_ylim(axes_spec.ylim)
    if axes_spec.aspect is not None:
        ax.set_aspect(axes_spec.aspect, adjustable="box")
    if axes_spec.grid:
        ax.grid(True, alpha=axes_spec.grid_alpha)
    if spec.colorbar:
        figure.colorbar(mappable, ax=ax, label=spec.colorbar_label)
    if spec.figure.tight_layout:
        figure.tight_layout()
    return RenderResult(figure=figure, axes=ax, artists=tuple(artists))


def render_vector_field(spec: VectorFieldPlotSpec, *, ax=None) -> RenderResult:
    """Render an explicit x-first arrow or headless director field."""

    import matplotlib.pyplot as plt

    if ax is None:
        figure, ax = plt.subplots(figsize=spec.figure.figsize)
    else:
        figure = ax.figure
    sx, sy = spec.step
    ii = np.arange(0, len(spec.x), sx)
    jj = np.arange(0, len(spec.y), sy)
    X, Y = np.meshgrid(spec.x[ii], spec.y[jj], indexing="ij")
    U = spec.u[np.ix_(ii, jj)].copy()
    V = spec.v[np.ix_(ii, jj)].copy()
    if spec.style.normalize:
        magnitude = np.hypot(U, V)
        np.divide(U, magnitude, out=U, where=magnitude > 0)
        np.divide(V, magnitude, out=V, where=magnitude > 0)
        U[magnitude == 0] = 0.0
        V[magnitude == 0] = 0.0
    options = {
        "pivot": spec.style.pivot,
        "angles": "xy",
        "scale_units": "xy",
        "scale": spec.style.scale,
        "width": spec.style.width,
        "alpha": spec.style.alpha,
    }
    if spec.glyph == "director":
        options.update(headlength=0, headaxislength=0, headwidth=0)
    colors = None if spec.color_values is None else spec.color_values[np.ix_(ii, jj)]
    if spec.style.color is not None:
        quiver = ax.quiver(X, Y, U, V, color=spec.style.color, **options)
    elif colors is not None:
        quiver = ax.quiver(X, Y, U, V, colors, cmap=spec.style.cmap, **options)
        quiver.set_clim(spec.style.vmin, spec.style.vmax)
    else:
        quiver = ax.quiver(X, Y, U, V, **options)

    axes_spec = spec.axes
    ax.set_xlabel(axes_spec.xlabel)
    ax.set_ylabel(axes_spec.ylabel)
    ax.set_title(axes_spec.title)
    if axes_spec.xlim is not None:
        ax.set_xlim(axes_spec.xlim)
    if axes_spec.ylim is not None:
        ax.set_ylim(axes_spec.ylim)
    if axes_spec.aspect is not None:
        ax.set_aspect(axes_spec.aspect, adjustable="box")
    if axes_spec.grid:
        ax.grid(True, alpha=axes_spec.grid_alpha)
    if spec.figure.tight_layout:
        figure.tight_layout()
    return RenderResult(figure=figure, axes=ax, artists=(quiver,))


def _finite_range(arrays, vmin, vmax):
    finite = [np.asarray(values)[np.isfinite(values)] for values in arrays]
    finite = np.concatenate([values for values in finite if values.size]) if any(values.size for values in finite) else np.asarray([])
    if vmin is None:
        vmin = float(np.min(finite)) if finite.size else 0.0
    if vmax is None:
        vmax = float(np.max(finite)) if finite.size else 1.0
    if vmax == vmin:
        delta = 1.0 if vmin == 0 else abs(vmin) * 1e-9
        vmin -= delta
        vmax += delta
    return vmin, vmax


def render_multi_surface_3d(spec: MultiSurfacePlotSpec, *, ax=None) -> RenderResult:
    """Render physical-height surface layers without output side effects."""

    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize

    if ax is None:
        figure = plt.figure(figsize=spec.figure.figsize)
        ax = figure.add_subplot(111, projection="3d")
    else:
        figure = ax.figure
    X, Y = np.meshgrid(spec.x, spec.y, indexing="xy")
    color_fields = [
        layer.z if layer.color_values is None else layer.color_values
        for layer in spec.layers
    ]
    vmin, vmax = _finite_range(color_fields, spec.style.vmin, spec.style.vmax)
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
    cmap = plt.get_cmap(spec.style.cmap)
    surfaces = []
    for layer, color_values in zip(spec.layers, color_fields):
        if layer.rgba is None:
            colors = np.asarray(cmap(norm(color_values)), dtype=float)
        else:
            colors = np.asarray(layer.rgba, dtype=float).copy()
        if layer.alpha_values is None:
            alpha_values = np.full_like(layer.z, layer.alpha, dtype=float)
        else:
            amin, amax = _finite_range(
                (layer.alpha_values,), layer.alpha_vmin, layer.alpha_vmax
            )
            alpha_values = Normalize(amin, amax, clip=True)(layer.alpha_values) * layer.alpha
        colors[..., 3] *= np.clip(alpha_values, 0.0, 1.0)
        invalid = ~np.isfinite(layer.z) | ~np.isfinite(color_values)
        if layer.alpha_values is not None:
            invalid |= ~np.isfinite(layer.alpha_values)
        colors[invalid, 3] = 0.0
        surface = ax.plot_surface(
            X,
            Y,
            layer.z.T,
            facecolors=np.transpose(colors, (1, 0, 2)),
            rstride=spec.style.rstride,
            cstride=spec.style.cstride,
            shade=spec.style.shade,
        )
        surface.set_cmap(cmap)
        surface.set_norm(norm)
        # Deliberately NO set_array() here: facecolors above are already the
        # rendered truth. Setting an array makes Poly3DCollection recompute
        # facecolors at draw time, which (a) degrades NaN cells to the cmap
        # bad color instead of the transparent holes prepared above, and
        # (b) explodes SVG export memory on dense grids (~3 GiB
        # Poly3DCollection allocation at >=100x100). The artist keeps its
        # cmap+norm, so get_clim()/colorbar use remains intact.
        surfaces.append(surface)
    ax.set_xlabel(spec.xlabel)
    ax.set_ylabel(spec.ylabel)
    ax.set_zlabel(spec.zlabel)
    ax.view_init(elev=spec.elev, azim=spec.azim)
    ax.set_box_aspect(spec.box_aspect)
    if spec.figure.tight_layout:
        figure.tight_layout()
    return RenderResult(figure=figure, axes=ax, artists=tuple(surfaces))


def _grid_field(x, y, values, *, name: str):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    values = np.asarray(values, dtype=float)
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be one-dimensional")
    expected = (len(x), len(y))
    if values.shape != expected:
        raise ValueError(f"{name} must have shape {expected}, got {values.shape}")
    return x, y, values


def render_polarization_ellipses(
    x,
    y,
    s1,
    s2,
    s3,
    *,
    ax=None,
    step=(6, 6),
    scale=None,
    cmap="RdBu",
    clim=(-1.0, 1.0),
    linewidth=1.2,
    alpha=0.9,
    zorder=2,
) -> RenderResult:
    """Render a sampled Stokes field as polarization ellipse patches."""

    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Ellipse

    x, y, s1 = _grid_field(x, y, s1, name="s1")
    _, _, s2 = _grid_field(x, y, s2, name="s2")
    _, _, s3 = _grid_field(x, y, s3, name="s3")
    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = ax.figure
    phi = (0.5 * np.arctan2(s2, s1) + np.pi / 2) % np.pi - np.pi / 2
    chi = 0.5 * np.arcsin(np.clip(s3, -1.0, 1.0))
    dx = np.min(np.diff(x)) if x.size > 1 else 1.0
    dy = np.min(np.diff(y)) if y.size > 1 else 1.0
    if scale is None:
        scale = 0.8 * min(abs(dx), abs(dy))
    sx, sy = step if isinstance(step, (tuple, list)) else (step, step)
    patches, colors = [], []
    for i in range(0, len(x), max(1, int(sx))):
        for j in range(0, len(y), max(1, int(sy))):
            if not np.all(np.isfinite([phi[i, j], chi[i, j], s3[i, j]])):
                continue
            minor = max(scale * abs(np.tan(chi[i, j])), 1e-3 * scale)
            patches.append(
                Ellipse(
                    (x[i], y[j]),
                    width=scale,
                    height=minor,
                    angle=np.degrees(phi[i, j]),
                )
            )
            colors.append(s3[i, j])
    collection = PatchCollection(
        patches,
        linewidths=linewidth,
        alpha=alpha,
        zorder=zorder,
        cmap=cmap,
    )
    if colors:
        collection.set_array(np.asarray(colors))
        collection.set_clim(*clim)
        collection.set_edgecolor(collection.cmap(collection.norm(colors)))
        collection.set_facecolor(collection.cmap(collection.norm(colors)))
    ax.add_collection(collection)
    ax.set_xlim(float(np.min(x)), float(np.max(x)))
    ax.set_ylim(float(np.min(y)), float(np.max(y)))
    ax.set_aspect("equal", adjustable="box")
    return RenderResult(figure=figure, axes=ax, artists=(collection,))


def render_polarization_angles(
    x,
    y,
    phi,
    chi,
    *,
    ax=None,
    step=(2, 2),
    scale=None,
    color_by="chi",
    cmap=None,
    clim=None,
    edgecolor="k",
    linewidth=2,
    alpha=0.9,
    zorder=2,
) -> RenderResult:
    """Render orientation and normalized helicity fields as ellipse patches."""

    import matplotlib.pyplot as plt
    from matplotlib import colormaps
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Ellipse

    x, y, phi = _grid_field(x, y, phi, name="phi")
    _, _, chi = _grid_field(x, y, chi, name="chi")
    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = ax.figure
    phi = (phi + np.pi / 2) % np.pi - np.pi / 2
    dx = np.min(np.diff(x)) if x.size > 1 else 1.0
    dy = np.min(np.diff(y)) if y.size > 1 else 1.0
    if scale is None:
        scale = 0.8 * min(abs(dx), abs(dy))

    sx, sy = step if isinstance(step, (tuple, list)) else (step, step)
    patches = []
    colors = []
    for i in range(0, len(x), max(1, int(sx))):
        for j in range(0, len(y), max(1, int(sy))):
            if not np.all(np.isfinite([phi[i, j], chi[i, j]])):
                continue
            helicity = np.clip(chi[i, j], -1.0, 1.0)
            ellipticity = 0.5 * np.arcsin(helicity)
            minor = max(scale * abs(np.tan(ellipticity)), 1e-3 * scale)
            patches.append(
                Ellipse(
                    (x[i], y[j]),
                    width=scale,
                    height=minor,
                    angle=np.degrees(phi[i, j]),
                )
            )
            if color_by == "chi":
                colors.append(helicity)
            elif color_by == "phi":
                colors.append((phi[i, j] + np.pi / 2) % np.pi)
            else:
                colors.append(0.0)

    collection = PatchCollection(
        patches,
        facecolor="none",
        edgecolor=edgecolor,
        linewidths=linewidth,
        alpha=alpha,
        zorder=zorder,
    )
    if color_by in {"chi", "phi"} and colors:
        if cmap is None:
            cmap = "RdBu" if color_by == "chi" else "twilight"
        if clim is None:
            clim = (-1.0, 1.0) if color_by == "chi" else (0.0, np.pi)
        values = np.asarray(colors, dtype=float)
        normalized = (values - clim[0]) / (clim[1] - clim[0] + 1e-12)
        mapped = colormaps[cmap](np.clip(normalized, 0.0, 1.0))
        collection.set_facecolor(mapped)
        collection.set_edgecolor(mapped)
    ax.add_collection(collection)
    ax.set_aspect("equal", adjustable="box")
    return RenderResult(figure=figure, axes=ax, artists=(collection,))


def _poincare_sphere(ax, style):
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, np.pi, 60)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    if style == "surface":
        return ax.plot_surface(x, y, z, rstride=4, cstride=4, color="lightgray", alpha=0.15, linewidth=0)
    return ax.plot_wireframe(x, y, z, rstride=6, cstride=6, color="lightgray", linewidth=0.5, alpha=0.6)


def render_poincare_scatter(
    s1,
    s2,
    s3,
    *,
    ax=None,
    rgba=None,
    step=(4, 4),
    color_by="s3",
    cmap="RdBu",
    clim=(-1.0, 1.0),
    size=6,
    alpha=0.9,
    sphere_style="wire",
) -> RenderResult:
    """Render a 2D Stokes field as sampled points on a Poincare sphere."""

    import matplotlib.pyplot as plt

    s1, s2, s3 = np.broadcast_arrays(
        np.asarray(s1, dtype=float), np.asarray(s2, dtype=float), np.asarray(s3, dtype=float)
    )
    if s1.ndim != 2:
        raise ValueError("Poincare scatter fields must be two-dimensional")
    if ax is None:
        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")
    else:
        figure = ax.figure
        if not hasattr(ax, "get_zlim"):
            raise ValueError("Poincare rendering requires a 3D axes")
    sy, sx = step if isinstance(step, (tuple, list)) else (step, step)
    yy = np.arange(0, s1.shape[0], max(1, int(sy)))
    xx = np.arange(0, s1.shape[1], max(1, int(sx)))
    sampled = [component[np.ix_(yy, xx)] for component in (s1, s2, s3)]
    points = np.column_stack([component.ravel() for component in sampled])
    valid = np.all(np.isfinite(points), axis=1)
    points = points[valid]
    sphere = _poincare_sphere(ax, sphere_style)
    options = {"s": size, "alpha": alpha, "depthshade": False}
    if color_by == "rgba":
        if rgba is None:
            raise ValueError("color_by='rgba' requires rgba")
        colors = np.asarray(rgba)[np.ix_(yy, xx)].reshape(-1, 4)[valid]
        options["c"] = colors
    elif color_by == "phi":
        options.update(
            c=(0.5 * np.arctan2(points[:, 1], points[:, 0])) % np.pi,
            cmap="twilight",
            vmin=0.0,
            vmax=np.pi,
        )
    elif color_by == "s3":
        options.update(c=np.clip(points[:, 2], -1, 1), cmap=cmap, vmin=clim[0], vmax=clim[1])
    else:
        raise ValueError("color_by must be 's3', 'phi', or 'rgba'")
    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], **options)
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_zlim(-1.05, 1.05)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])
    return RenderResult(figure=figure, axes=ax, artists=(sphere, scatter))


def render_poincare_trajectory(
    s1,
    s2,
    s3,
    *,
    ax=None,
    cmap="rainbow",
    linewidth=2.0,
    sphere_style="wire",
) -> RenderResult:
    """Render a one-dimensional trajectory on a Poincare sphere."""

    import matplotlib.pyplot as plt

    points = np.column_stack((s1, s2, s3)).astype(float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("trajectory components must be equal-length 1D arrays")
    valid = np.all(np.isfinite(points), axis=1)
    points = points[valid]
    if ax is None:
        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")
    else:
        figure = ax.figure
    sphere = _poincare_sphere(ax, sphere_style)
    colors = plt.get_cmap(cmap)(np.linspace(0, 1, max(len(points) - 1, 1)))
    lines = []
    for index in range(len(points) - 1):
        lines.extend(ax.plot(*points[index:index + 2].T, color=colors[index], linewidth=linewidth))
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_zlim(-1.05, 1.05)
    return RenderResult(figure=figure, axes=ax, artists=(sphere, *lines))


def render_surface_3d(x, y, values, *, ax=None, cmap="viridis", alpha=1.0) -> RenderResult:
    """Render an explicit xy-oriented scalar grid as a 3D surface."""

    import matplotlib.pyplot as plt

    x, y, values = _grid_field(x, y, values, name="values")
    if ax is None:
        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")
    else:
        figure = ax.figure
    X, Y = np.meshgrid(x, y, indexing="xy")
    surface = ax.plot_surface(X, Y, values.T, cmap=cmap, alpha=alpha)
    return RenderResult(figure=figure, axes=ax, artists=(surface,))
