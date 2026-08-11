"""Compatibility contour and path renderers."""

from __future__ import annotations

import warnings

import numpy as np


def extract_contour_paths(xgrid, ygrid, values, level):
    """Extract x-first contour segments while closing the temporary figure."""

    import matplotlib.pyplot as plt

    x_values = np.asarray(xgrid)
    y_values = np.asarray(ygrid)
    field = np.asarray(values, dtype=float)
    expected = (x_values.size, y_values.size)
    if field.ndim != 2 or field.shape != expected:
        raise ValueError(f"values shape must be {expected}, got {field.shape}")
    if np.isnan(field).any():
        field = np.ma.array(field, mask=np.isnan(field))
    minimum = float(np.nanmin(field))
    maximum = float(np.nanmax(field))
    if not minimum <= level <= maximum:
        warnings.warn(
            f"contour level {level} is outside [{minimum:.6g}, {maximum:.6g}]",
            stacklevel=2,
        )
        return []
    if np.allclose(field, level, atol=0, rtol=0):
        level = float(level) + 1e-12
    X, Y = np.meshgrid(x_values, y_values, indexing="ij")
    figure, ax = plt.subplots()
    try:
        contour = ax.contour(X, Y, field, levels=[level])
        paths = []
        if hasattr(contour, "allsegs") and contour.allsegs:
            for segment in contour.allsegs[0]:
                segment = np.asarray(segment)
                if segment.ndim == 2 and segment.shape[0] >= 2 and segment.shape[1] == 2:
                    paths.append(segment.copy())
        return paths
    finally:
        plt.close(figure)


extract_isofreq_paths = extract_contour_paths


def plot_iso_contours2D(
    ax,
    xgrid,
    ygrid,
    values,
    levels,
    colors=None,
    linewidths=1,
    linestyles="-",
    return_paths=True,
    **contour_kwargs,
):
    """Draw historical x-first contours and preserve the legacy return contract."""

    x_values = np.asarray(xgrid)
    y_values = np.asarray(ygrid)
    field = np.asarray(values, dtype=float)
    expected = (x_values.size, y_values.size)
    if field.shape != expected:
        raise ValueError(f"values shape {field.shape} != {expected}")
    if np.isnan(field).any():
        field = np.ma.array(field, mask=np.isnan(field))
    X, Y = np.meshgrid(x_values, y_values, indexing="ij")
    contour = ax.contour(
        X,
        Y,
        field,
        levels=np.atleast_1d(levels),
        colors=colors,
        linewidths=linewidths,
        linestyles=linestyles,
        **contour_kwargs,
    )
    if not return_paths:
        return contour
    return ax


def plot_paths(ax, paths, colors="C0", linewidth=2.0, alpha=1.0, labels=None, zorder=3):
    """Draw a list or level mapping of two-column paths and return Line2D artists."""

    all_paths = []
    if isinstance(paths, dict):
        for path_list in paths.values():
            all_paths.extend(path_list)
    else:
        all_paths = list(paths)
    color_list = list(colors) if isinstance(colors, (list, tuple, np.ndarray)) else None
    lines = []
    for index, path in enumerate(all_paths):
        points = np.asarray(path)
        color = color_list[index] if color_list and index < len(color_list) else colors
        label = labels[index] if labels and index < len(labels) else None
        line, = ax.plot(
            points[:, 0],
            points[:, 1],
            color=color,
            lw=linewidth,
            alpha=alpha,
            label=label,
            zorder=zorder,
        )
        lines.append(line)
    return lines


__all__ = [
    "extract_contour_paths",
    "extract_isofreq_paths",
    "plot_iso_contours2D",
    "plot_paths",
]
