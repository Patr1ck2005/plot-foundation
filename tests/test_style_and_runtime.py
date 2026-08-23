from __future__ import annotations

from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

from plot_foundation import (
    DIAGNOSTIC_PROFILE,
    PAPER_PROFILE,
    PREVIEW_PROFILE,
    PUBLICATION_MINIMAL_PROFILE,
    FigureConfig,
    FigurePolicy,
    SaveSpec,
    apply_style,
    profile,
    profile_context,
    runtime_info,
    save_figure,
    style_context,
    __version__,
)


def test_apply_style_matches_agent_glue_dicts():
    """The imperative one-call bridge must reproduce the minimal Arial-9 dict
    that project _lib_common modules hand-copied (agent_kit.AGG_RC_PARAMS)."""
    import matplotlib as mpl

    apply_style()
    assert mpl.rcParams["font.size"] == 9
    assert mpl.rcParams["font.family"] == ["sans-serif"]
    assert list(mpl.rcParams["font.sans-serif"])[:2] == ["Arial", "DejaVu Sans"]
    assert mpl.rcParams["xtick.direction"] == "in"
    assert mpl.rcParams["ytick.direction"] == "in"


def test_style_context_is_scoped():
    import matplotlib as mpl

    before = mpl.rcParams["font.size"]
    with style_context():
        assert mpl.rcParams["font.size"] == 9
        mpl.rcParams["font.size"] = 17
    assert mpl.rcParams["font.size"] == before


def test_profile_context_is_scoped_and_resolves_named_profile():
    import matplotlib as mpl

    before = mpl.rcParams["font.size"]
    with profile_context("publication_minimal"):
        assert mpl.rcParams["font.size"] == 9
        assert mpl.rcParams["figure.autolayout"] is False
        assert mpl.rcParams["figure.constrained_layout.use"] is False
    assert mpl.rcParams["font.size"] == before


def test_save_requires_caller_owned_parent(tmp_path):
    import matplotlib.pyplot as plt

    figure, _ = plt.subplots()
    with pytest.raises(FileNotFoundError, match="caller owns directories"):
        save_figure(figure, tmp_path / "missing" / "plot.png")
    target = save_figure(figure, tmp_path / "plot.png", SaveSpec(dpi=100))
    assert target.is_file()
    assert SaveSpec.paper().dpi == 300
    assert SaveSpec.preview().dpi == 150
    assert PAPER_PROFILE.name == "paper"
    assert PREVIEW_PROFILE.save.transparent is True


def test_publication_and_diagnostic_policies_are_explicit():
    publication = PUBLICATION_MINIMAL_PROFILE.policy
    assert publication == FigurePolicy.publication_minimal()
    assert publication.show_title is False
    assert publication.show_axis_labels is False
    assert publication.show_legend is False
    assert publication.show_colorbar is False
    assert publication.grid is False
    assert publication.tight_layout is False

    diagnostic = DIAGNOSTIC_PROFILE.policy
    assert diagnostic == FigurePolicy.diagnostic()
    assert diagnostic.show_title is True
    assert diagnostic.grid is True
    assert diagnostic.tight_layout is True
    assert profile("paper").policy == publication


def test_figure_config_resolves_profile_policy():
    config = FigureConfig(style_profile="diagnostic")
    assert config.resolved_profile is DIAGNOSTIC_PROFILE
    assert config.resolved_policy.grid is True
    assert config.resolved_save.dpi == 150


def test_save_spec_round_trip():
    spec = SaveSpec(dpi=210, bbox_inches=None, transparent=False)
    assert SaveSpec.from_dict(spec.to_dict()) == spec


def test_runtime_reports_source_tree():
    info = runtime_info()
    assert info.distribution == "plot-foundation"
    assert info.version == __version__
    assert Path(info.module_file).name == "runtime.py"
