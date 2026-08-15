from __future__ import annotations

from pathlib import Path

import numpy as np

from plot_foundation import (
    HeatmapPlotSpec,
    MultiSurfacePlotSpec,
    SurfaceLayer,
)


CANONICAL_SPEC_URL = (
    "https://github.com/Patr1ck2005/plot-workflows/blob/main/"
    "docs/data-space-and-visualization.md"
)


def test_same_x_first_2d_grid_supports_heatmap_and_surface_views():
    x = np.asarray([-1.0, 0.5, 2.0])
    y = np.asarray([-2.0, 1.0])
    values = np.asarray([[10.0, 11.0], [20.0, 21.0], [30.0, 31.0]])

    heatmap = HeatmapPlotSpec(x=x, y=y, values=values)
    surface = MultiSurfacePlotSpec(
        x=x,
        y=y,
        layers=(SurfaceLayer(z=values),),
    )

    assert heatmap.values.shape == (len(x), len(y))
    assert surface.layers[0].z.shape == (len(x), len(y))
    np.testing.assert_array_equal(heatmap.values, surface.layers[0].z)


def test_agent_entry_links_canonical_data_space_specification():
    agents = (Path(__file__).parents[1] / "AGENTS.md").read_text(encoding="utf-8")
    normalized = " ".join(agents.split())

    assert CANONICAL_SPEC_URL in agents
    assert "intrinsic data dimension" in normalized
    assert "sampling topology" in normalized
    assert "Rendering dimension does not determine data dimension" in normalized
