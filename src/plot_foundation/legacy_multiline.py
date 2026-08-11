"""Historical complex one- and two-dimensional multiline renderers."""

from __future__ import annotations

import numpy as np

from .legacy_line import plot_line_advanced


def plot_1d_lines(ax, x_vals, y_vals_list, plot_params):
    default_colors = plot_params.get("default_color_list")
    enable_fill = plot_params.get("enable_line_fill", True)
    scale = plot_params.get("scale", 0.5)
    y_mins, y_maxs = [], []
    for index, y_values in enumerate(y_vals_list):
        if default_colors is not None:
            plot_params["default_color"] = default_colors[index % len(default_colors)]
        y_values = np.asarray(y_values)
        ax = plot_line_advanced(
            ax,
            x_vals,
            z1=y_values.real,
            z2=y_values.imag,
            z3=y_values.imag,
            **plot_params,
        )
        widths = np.abs(y_values.imag)
        if enable_fill:
            y_mins.append(np.min(y_values.real - scale * widths))
            y_maxs.append(np.max(y_values.real + scale * widths))
        else:
            y_mins.append(np.min(y_values.real))
            y_maxs.append(np.max(y_values.real))
    x_values = np.asarray(x_vals)
    ax.set_xlim(x_values.min(), x_values.max())
    ax.set_ylim(np.nanmin(y_mins) * 0.98, np.nanmax(y_maxs) * 1.02)
    if plot_params.get("log_scale", False):
        ax.set_yscale("log")
    return ax.get_figure(), ax


def plot_2d_multiline(ax, x_vals, y_vals, values, plot_params):
    from matplotlib import colormaps
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize

    x_values = np.asarray(x_vals)
    y_values = np.asarray(y_vals)
    field = np.asarray(values)
    cmap = colormaps.get_cmap(plot_params.get("cmap", "viridis"))
    default_color = plot_params.get("default_color")
    default_colors = plot_params.get("default_color_list")
    alpha = plot_params.get("alpha", 1.0)
    plot_imaginary = plot_params.get("imag", False)
    add_colorbar = plot_params.get("add_colorbar", False)
    color_min = plot_params.get("global_color_vmin", y_values.min())
    color_max = plot_params.get("global_color_vmax", y_values.max())
    linewidth = plot_params.get("linewidth")
    norm = Normalize(vmin=color_min, vmax=color_max)
    real = field.real
    imaginary = field.imag if np.iscomplexobj(field) else np.zeros_like(real)
    y_mins, y_maxs = [], []
    for index, parameter in enumerate(y_values):
        if default_color is not None:
            color = default_color
        elif default_colors is not None:
            color = default_colors[index % len(default_colors)]
        else:
            color = cmap(norm(parameter))
        ax.plot(
            x_values,
            real[:, index],
            label=f"Real (y={parameter:.2f})",
            color=color,
            alpha=alpha,
            linewidth=linewidth,
        )
        y_mins.append(np.nanmin(real[:, index]))
        y_maxs.append(np.nanmax(real[:, index]))
        if np.iscomplexobj(field) and plot_imaginary and np.abs(imaginary[:, index]).max() > 1e-8:
            ax.plot(
                x_values,
                imaginary[:, index],
                label=f"Imag (y={parameter:.2f})",
                color=color,
                linestyle="--",
                alpha=alpha,
                linewidth=linewidth,
            )
            y_mins.append(np.nanmin(imaginary[:, index]))
            y_maxs.append(np.nanmax(imaginary[:, index]))
    ax.set_xlim(x_values.min(), x_values.max())
    ax.set_ylim(np.nanmin(y_mins) * 0.98, np.nanmax(y_maxs) * 1.02)
    if add_colorbar and default_color is None and default_colors is None:
        mappable = ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array(y_values)
        ax.get_figure().colorbar(mappable, ax=ax)
    return ax.get_figure(), ax


__all__ = ["plot_1d_lines", "plot_2d_multiline"]
