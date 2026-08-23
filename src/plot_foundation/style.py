"""Scoped Matplotlib style, figure presets, and explicit save policy."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MatplotlibStyle:
    """Portable defaults distilled from consumer plotting experience."""

    font_size: float = 9.0
    font_family: str = "sans-serif"
    sans_serif: tuple[str, ...] = ("Arial", "DejaVu Sans")
    xtick_direction: str = "in"
    ytick_direction: str = "in"
    axes_grid: bool = False
    lines_linewidth: float = 1.0

    def rc(self) -> dict:
        return {
            "font.size": self.font_size,
            "font.family": self.font_family,
            "font.sans-serif": list(self.sans_serif),
            "xtick.direction": self.xtick_direction,
            "ytick.direction": self.ytick_direction,
            "axes.grid": self.axes_grid,
            "lines.linewidth": self.lines_linewidth,
            "figure.autolayout": False,
            "figure.constrained_layout.use": False,
        }

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class FigurePreset:
    """Semantic figure geometry, kept separate from data and renderer code."""

    name: str
    figsize: tuple[float, float]


_FIGURE_PRESETS = {
    "single": (1.5, 1.5),
    "overview_3d": (2.0, 2.0),
    "line": (4.0, 3.0),
}


def figure_preset(name: str, *, rows: int = 1, cols: int = 1) -> FigurePreset:
    """Return a named geometry preset.

    ``summary_panel`` uses the paper protocol's 1.5-inch panel unit and scales
    it by the requested row/column count.
    """

    if name == "summary_panel":
        if rows <= 0 or cols <= 0:
            raise ValueError("summary_panel rows and cols must be positive")
        return FigurePreset(name, (1.5 * cols, 1.5 * rows))
    try:
        figsize = _FIGURE_PRESETS[name]
    except KeyError as exc:
        raise ValueError(f"unknown figure preset: {name!r}") from exc
    return FigurePreset(name, figsize)


PAPER_STYLE = MatplotlibStyle()
PAPER_FIGURE = figure_preset("single")
OVERVIEW_FIGURE = figure_preset("overview_3d")


def style_context(style: MatplotlibStyle = PAPER_STYLE):
    """Return a context manager that restores Matplotlib state on exit."""

    import matplotlib as mpl

    return mpl.rc_context(rc=style.rc())


def apply_style(style: MatplotlibStyle = PAPER_STYLE) -> None:
    """Apply a style's rcParams globally (imperative one-call for scripts).

    Project ``_lib_common`` modules call this once at import instead of
    hand-copying rcParams dicts; use :func:`style_context` when a scoped,
    restorable change is needed. Note the full paper style also pins
    ``lines.linewidth: 1.0`` and disables auto-layout — stricter than the
    minimal five-key dicts some projects carry.
    """

    import matplotlib as mpl

    mpl.rcParams.update(style.rc())


@dataclass(frozen=True)
class SaveSpec:
    """Explicit save policy; layout remains separate from output cropping."""

    dpi: int = 300
    bbox_inches: str | None = "tight"
    transparent: bool = True

    def __post_init__(self) -> None:
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    @classmethod
    def paper(cls) -> "SaveSpec":
        return cls(dpi=300, bbox_inches="tight", transparent=True)

    @classmethod
    def preview(cls) -> "SaveSpec":
        return cls(dpi=150, bbox_inches="tight", transparent=True)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, values: dict) -> "SaveSpec":
        return cls(**dict(values))


@dataclass(frozen=True)
class FigurePolicy:
    """Domain-neutral defaults for publication and diagnostic figures.

    The policy controls presentation choices only. Physical decisions such as
    axis limits, equal data aspect, color normalization, and colormaps remain
    explicit in each plot specification or consumer workflow.
    """

    show_title: bool = True
    show_axis_labels: bool = True
    show_legend: bool = True
    show_colorbar: bool = True
    grid: bool = False
    tight_layout: bool = False

    @classmethod
    def publication_minimal(cls) -> "FigurePolicy":
        return cls(
            show_title=False,
            show_axis_labels=False,
            show_legend=False,
            show_colorbar=False,
            grid=False,
            tight_layout=False,
        )

    @classmethod
    def diagnostic(cls) -> "FigurePolicy":
        return cls(
            show_title=True,
            show_axis_labels=True,
            show_legend=True,
            show_colorbar=True,
            grid=True,
            tight_layout=True,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, values: dict) -> "FigurePolicy":
        return cls(**dict(values))


@dataclass(frozen=True)
class PlotProfile:
    """A named pairing of scoped style, save policy, and figure defaults."""

    name: str
    style: MatplotlibStyle
    save: SaveSpec
    policy: FigurePolicy = FigurePolicy()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "style": self.style.to_dict(),
            "save": self.save.to_dict(),
            "policy": self.policy.to_dict(),
        }


PUBLICATION_MINIMAL_PROFILE = PlotProfile(
    "publication_minimal",
    PAPER_STYLE,
    SaveSpec.paper(),
    FigurePolicy.publication_minimal(),
)
PAPER_PROFILE = PlotProfile(
    "paper",
    PAPER_STYLE,
    SaveSpec.paper(),
    FigurePolicy.publication_minimal(),
)
PREVIEW_PROFILE = PlotProfile(
    "preview",
    PAPER_STYLE,
    SaveSpec.preview(),
    FigurePolicy.publication_minimal(),
)
DIAGNOSTIC_PROFILE = PlotProfile(
    "diagnostic",
    PAPER_STYLE,
    SaveSpec.preview(),
    FigurePolicy.diagnostic(),
)


def profile(name: str) -> PlotProfile:
    """Resolve a stable profile name for consumer configuration."""

    try:
        return {
            "paper": PAPER_PROFILE,
            "publication_minimal": PUBLICATION_MINIMAL_PROFILE,
            "preview": PREVIEW_PROFILE,
            "diagnostic": DIAGNOSTIC_PROFILE,
        }[name]
    except KeyError as exc:
        raise ValueError(f"unknown plot profile: {name!r}") from exc


def profile_context(value: str | PlotProfile = "paper"):
    """Return a scoped Matplotlib context for a named or resolved profile."""

    resolved = profile(value) if isinstance(value, str) else value
    return style_context(resolved.style)


def save_figure(figure, path: str | Path, spec: SaveSpec = SaveSpec()) -> Path:
    """Save to an existing parent directory without closing the figure."""

    target = Path(path)
    if not target.parent.is_dir():
        raise FileNotFoundError(
            f"output parent does not exist; caller owns directories: {target.parent}"
        )
    figure.savefig(
        target,
        dpi=spec.dpi,
        bbox_inches=spec.bbox_inches,
        transparent=spec.transparent,
    )
    return target
