"""Domain-neutral artists for fitted curves and classified path segments."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

import numpy as np


def plot_lineshape_comparison(
    ax,
    x: Sequence[float],
    y: Sequence[float],
    lorentzian_result: Any,
    fano_result: Any,
    *,
    best_result: Any | None = None,
    scatter_kwargs: Mapping[str, Any] | None = None,
    lorentzian_kwargs: Mapping[str, Any] | None = None,
    fano_kwargs: Mapping[str, Any] | None = None,
):
    """Draw data and two fit-result objects on a caller-owned axes."""

    scatter_options = {"s": 16, "alpha": 0.8, "label": "Data"}
    scatter_options.update(scatter_kwargs or {})
    lorentzian_options = {"lw": 2, "label": "Lorentzian fit"}
    lorentzian_options.update(lorentzian_kwargs or {})
    fano_options = {"lw": 2, "linestyle": "--", "label": "Fano fit"}
    fano_options.update(fano_kwargs or {})

    ax.scatter(np.asarray(x), np.asarray(y), **scatter_options)
    ax.plot(lorentzian_result.x_fit, lorentzian_result.y_fit, **lorentzian_options)
    ax.plot(fano_result.x_fit, fano_result.y_fit, **fano_options)
    title = "Lineshape Fit Comparison"
    if best_result is not None:
        title += f"  (best: {best_result.model})"
    ax.set(title=title, xlabel="x", ylabel="y")
    ax.legend()
    return ax

def plot_field_regime_splits(
    ax,
    splits: Mapping[str, Sequence[np.ndarray]],
    *,
    color_phi0: str = "limegreen",
    color_phi90: str = "black",
    color_uncertain: str = "orange",
    linewidth: float = 2.0,
):
    """Draw preclassified ``phi0``, ``phi90``, and ``uncertain`` segments."""

    styles = {
        "phi0": {"color": color_phi0, "lw": linewidth, "label": r"$\phi\approx 0,\pi$"},
        "phi90": {"color": color_phi90, "lw": linewidth, "label": r"$\phi\approx \pi/2$"},
        "uncertain": {
            "color": color_uncertain,
            "lw": linewidth,
            "ls": "--",
            "label": "uncertain",
        },
    }
    for family, options in styles.items():
        for segment in splits.get(family, ()):
            points = np.asarray(segment)
            if points.ndim != 2 or points.shape[1] != 2:
                raise ValueError(f"{family} segments must have shape (n, 2)")
            ax.plot(points[:, 0], points[:, 1], **options)
    return ax
