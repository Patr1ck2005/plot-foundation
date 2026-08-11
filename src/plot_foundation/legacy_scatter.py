"""Compatibility renderer for an advanced scatter API."""

from __future__ import annotations

import numpy as np


def plot_scatter_advanced(ax, x_vals, z1, z2=None, z3=None, index=0, **kwargs):
    """Render size- and color-mapped scatter points and return the caller's axes."""

    from matplotlib import colormaps
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable

    enable_size_variation = kwargs.get("enable_size_variation", False)
    enable_dynamic_color = kwargs.get("enable_dynamic_color", False)
    scale = kwargs.get("scale", 1.0)
    alpha = kwargs.get("alpha", 0.8)
    cmap = kwargs.get("cmap", "RdBu" if enable_dynamic_color else "Blues")
    if isinstance(cmap, str):
        cmap = colormaps.get_cmap(cmap)
    default_color = kwargs.get("default_color", "blue")
    size_base = kwargs.get("s_base", 50)
    edge_color = kwargs.get("edge_color", "black")
    add_colorbar = kwargs.get("add_colorbar", False)
    linewidth = kwargs.get("linewidth", 0.5)
    color_max = kwargs.get("global_color_vmax")
    color_min = kwargs.get("global_color_vmin")

    x_values = np.asarray(x_vals)
    y_values = np.asarray(z1)
    n = len(x_values)
    if len(y_values) != n:
        raise ValueError("z1 length must match x_vals")
    if z2 is not None and len(z2) != n:
        raise ValueError("z2 length must match x_vals")
    if z3 is not None and len(z3) != n:
        raise ValueError("z3 length must match x_vals")

    sizes = np.full(n, size_base)
    if z2 is not None and enable_size_variation:
        sizes = size_base + scale * np.abs(z2)
    color_values = np.asarray(z3) if z3 is not None else np.zeros(n)
    if color_max is not None and color_min is not None:
        norm = Normalize(vmin=color_min, vmax=color_max)
    else:
        norm = Normalize(vmin=np.min(color_values), vmax=np.max(color_values)) if z3 is not None else None

    options = {
        "s": sizes,
        "alpha": alpha,
        "edgecolors": edge_color,
        "linewidth": linewidth,
        **{key: value for key, value in kwargs.items() if key in {"marker", "linestyle", "zorder"}},
    }
    if enable_dynamic_color:
        if z3 is None:
            raise ValueError("dynamic color requires z3")
        ax.scatter(x_values, y_values, c=color_values, cmap=cmap, norm=norm, **options)
    else:
        if "default_color" not in kwargs:
            default_color = colormaps["tab10"](index % 10)
        ax.scatter(x_values, y_values, c=default_color, label="Scatter Points", **options)

    if add_colorbar and enable_dynamic_color and z3 is not None:
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        mappable.set_array(color_values)
        colorbar = ax.get_figure().colorbar(mappable, ax=ax)
        colorbar.set_label("z3 (controls point color)")

    ax.set_xlim(x_values.min(), x_values.max())
    y_min, y_max = y_values.min(), y_values.max()
    if enable_size_variation:
        margin = np.max(sizes) / 100
        y_min -= margin
        y_max += margin
    ax.set_ylim(y_min, y_max)
    return ax


__all__ = ["plot_scatter_advanced"]
