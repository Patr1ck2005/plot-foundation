"""Serializable per-figure configuration shared by plotting consumers."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import AxesSpec, FigureSpec
from .style import FigurePolicy, PlotProfile, SaveSpec, profile


@dataclass(frozen=True)
class FigureConfig:
    """Figure, axes, style profile, and save policy without filesystem state."""

    figure: FigureSpec = field(default_factory=FigureSpec)
    axes: AxesSpec = field(default_factory=AxesSpec)
    style_profile: str = "paper"
    save: SaveSpec | None = None

    def __post_init__(self) -> None:
        profile(self.style_profile)

    @property
    def resolved_save(self) -> SaveSpec:
        """Return the explicit save policy or the selected profile default."""

        return self.save if self.save is not None else profile(self.style_profile).save

    @property
    def resolved_profile(self) -> PlotProfile:
        return profile(self.style_profile)

    @property
    def resolved_policy(self) -> FigurePolicy:
        return self.resolved_profile.policy

    def to_dict(self) -> dict:
        return {
            "figure": self.figure.to_dict(),
            "axes": self.axes.to_dict(),
            "style_profile": self.style_profile,
            "save": self.save.to_dict() if self.save is not None else None,
        }

    @classmethod
    def from_dict(cls, values: dict) -> "FigureConfig":
        data = dict(values)
        save_values = data.get("save")
        data["figure"] = FigureSpec.from_dict(data.get("figure", {}))
        data["axes"] = AxesSpec.from_dict(data.get("axes", {}))
        data["save"] = SaveSpec.from_dict(save_values) if save_values is not None else None
        return cls(**data)
