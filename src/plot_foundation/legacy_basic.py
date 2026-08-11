"""Basic historical shape and axes-annotation helpers."""

from __future__ import annotations

import warnings


def draw_shapes(
    ax,
    x,
    y,
    plot_type="line",
    color="blue",
    marker=None,
    linestyle="-",
    alpha=1.0,
    label=None,
    hide_default_ticks=False,
    hide_default_ticklabels=False,
):
    """Draw one line, scatter, bar, or histogram on caller-owned axes."""

    if plot_type != "hist" and len(x) != len(y):
        raise ValueError("x and y lengths must match")
    if plot_type == "line":
        ax.plot(x, y, color=color, marker=marker, linestyle=linestyle, alpha=alpha, label=label)
    elif plot_type == "scatter":
        ax.scatter(x, y, color=color, marker=marker or "o", alpha=alpha, label=label)
    elif plot_type == "bar":
        ax.bar(x, y, color=color, alpha=alpha, label=label)
    elif plot_type == "hist":
        ax.hist(y, bins="auto", color=color, alpha=alpha, label=label)
    else:
        raise ValueError(f"unsupported plot_type: {plot_type}")
    if hide_default_ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    if hide_default_ticklabels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    return ax


def add_annotations(
    ax,
    title=None,
    xlabel=None,
    ylabel=None,
    xlim=None,
    ylim=None,
    show_legend=False,
    legend_loc="best",
    add_grid=False,
    grid_style="-",
    grid_alpha=0.5,
    xtick_mode="auto",
    xtick_count=None,
    xticks=None,
    xtick_labels=None,
    ytick_mode="auto",
    ytick_count=None,
    yticks=None,
    ytick_labels=None,
):
    """Apply the historical labels, limits, ticks, legend, and grid contract."""

    from matplotlib.ticker import MaxNLocator

    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    for axis, mode, count, ticks, labels in (
        (ax.xaxis, xtick_mode, xtick_count, xticks, xtick_labels),
        (ax.yaxis, ytick_mode, ytick_count, yticks, ytick_labels),
    ):
        if mode == "auto":
            continue
        if mode == "approx_count":
            if count is not None:
                axis.set_major_locator(MaxNLocator(nbins=count))
            continue
        if mode != "manual":
            raise ValueError(f"unsupported tick mode: {mode}")
        if ticks is None:
            warnings.warn("manual tick mode requested without tick positions", stacklevel=2)
            continue
        if axis is ax.xaxis:
            ax.set_xticks(ticks)
            if labels is not None:
                ax.set_xticklabels(labels)
        else:
            ax.set_yticks(ticks)
            if labels is not None:
                ax.set_yticklabels(labels)
    if show_legend:
        ax.legend(loc=legend_loc)
    if add_grid:
        ax.grid(True, linestyle=grid_style, alpha=grid_alpha)
    return ax


__all__ = ["draw_shapes", "add_annotations"]
