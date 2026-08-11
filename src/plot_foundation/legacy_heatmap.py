"""Compatibility renderer for an x-first ``imshow`` heatmap API."""

from __future__ import annotations

import numpy as np


def plot_2d_heatmap(ax, x_vals, y_vals, Z, plot_params):
    """Render the historical x-first complex grid and return ``(fig, ax)``."""

    cmap = plot_params.get("cmap", "viridis")
    alpha = plot_params.get("alpha", 1.0)
    aspect = plot_params.get("imshow_aspect", "auto")
    add_colorbar = plot_params.get("add_colorbar", False)
    colorbar_title = plot_params.get("title_colorbar", "")
    vmax = plot_params.get("global_color_vmax", None)
    vmin = plot_params.get("global_color_vmin", None)

    values = np.asarray(Z).real
    image = ax.imshow(
        values.T,
        extent=[x_vals[0], x_vals[-1], y_vals[0], y_vals[-1]],
        origin="lower",
        aspect=aspect,
        cmap=cmap,
        alpha=alpha,
        interpolation="none",
        vmin=vmin,
        vmax=vmax,
    )
    if add_colorbar:
        ax.get_figure().colorbar(image, ax=ax, label=colorbar_title)
    return ax.get_figure(), ax


__all__ = ["plot_2d_heatmap"]
