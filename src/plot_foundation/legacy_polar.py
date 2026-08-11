"""Historical polar-line and polarization scalar-map renderers."""

from __future__ import annotations

import numpy as np


def plot_polar_line(ax, angles, values, index=0, **kwargs):
    """Render radial values from degree or radian angles on polar axes."""

    from matplotlib import colormaps

    angle_values = np.asarray(angles)
    radial_values = np.asarray(values)
    if len(radial_values) != len(angle_values):
        raise ValueError("values length must match angles")
    unit = kwargs.get("angle_unit", "degrees")
    offset = kwargs.get("angle_offset_degrees", 0)
    if unit == "degrees":
        theta = np.deg2rad(angle_values + offset)
    elif unit == "radians":
        theta = angle_values + np.deg2rad(offset)
    else:
        raise ValueError("angle_unit must be 'degrees' or 'radians'")
    radial = np.maximum(0, radial_values) * kwargs.get("scale", 1.0)
    color = kwargs.get("default_color")
    if color is None:
        color = colormaps["tab10"](index % 10)
    ax.plot(
        theta,
        radial,
        color=color,
        linewidth=kwargs.get("linewidth_base", 1),
        alpha=kwargs.get("alpha_line", 0.8),
        label=f"Intensity {index + 1}",
    )
    if kwargs.get("set_r_lim", True):
        radial_max = kwargs.get("r_max")
        if radial_max is None:
            current = np.max(radial) if radial.size else 0
            radial_max = np.maximum(current * 1.1, 0.1)
        ax.set_rlim(kwargs.get("r_min", 0), radial_max)
    return ax


def imshow_phi(ax, phi, extent=None, vmin=-np.pi / 2, vmax=np.pi / 2, **imshow_kwargs):
    """Render an x-first orientation-angle field with its historical labels."""

    image = ax.imshow(
        np.asarray(phi).T,
        origin="lower",
        extent=extent,
        vmin=vmin,
        vmax=vmax,
        **imshow_kwargs,
    )
    ax.set_xlabel(r"$k_x$")
    ax.set_ylabel(r"$k_y$")
    ax.set_title(r"Orientation angle $\phi$")
    ax.get_figure().colorbar(image, ax=ax, shrink=0.8)
    return ax


def imshow_s3(ax, s3, S0=None, extent=None, vmin=-1.0, vmax=1.0, **imshow_kwargs):
    """Render an x-first S3 helicity field with its historical labels."""

    del S0
    image = ax.imshow(
        np.asarray(s3).T,
        origin="lower",
        extent=extent,
        vmin=vmin,
        vmax=vmax,
        **imshow_kwargs,
    )
    ax.set_xlabel(r"$k_x$")
    ax.set_ylabel(r"$k_y$")
    ax.set_title(r"$S_3$ (helicity)")
    ax.get_figure().colorbar(image, ax=ax, shrink=0.8)
    return ax


__all__ = ["plot_polar_line", "imshow_phi", "imshow_s3"]
