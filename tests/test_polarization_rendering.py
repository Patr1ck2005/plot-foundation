from __future__ import annotations

import numpy as np

from plot_foundation import (
    render_poincare_scatter,
    render_poincare_trajectory,
    render_polarization_ellipses,
    render_polarization_angles,
    render_surface_3d,
)


def _field():
    x = np.linspace(-1, 1, 5)
    y = np.linspace(-1, 1, 4)
    X, Y = np.meshgrid(x, y, indexing="ij")
    angle = np.arctan2(Y, X)
    return x, y, np.cos(angle), np.sin(angle), np.zeros_like(angle)


def test_polarization_ellipse_renderer_preserves_xy_grid_and_sampling():
    x, y, s1, s2, s3 = _field()
    result = render_polarization_ellipses(x, y, s1, s2, s3, step=(2, 2))
    assert len(result.artists[0].get_paths()) == 6
    assert result.axes.get_aspect() == 1.0
    np.testing.assert_allclose(result.axes.get_xlim(), [x.min(), x.max()])


def test_angle_ellipse_renderer_preserves_phi_chi_geometry_and_sampling():
    x = np.array([-1.0, 0.0, 1.0])
    y = np.array([-0.5, 0.5])
    phi = np.zeros((3, 2))
    phi[1, 1] = np.pi / 4
    chi = np.zeros((3, 2))
    chi[1, 1] = 1.0

    result = render_polarization_angles(
        x,
        y,
        phi,
        chi,
        step=(1, 1),
        scale=0.2,
        color_by="phi",
    )

    assert len(result.artists[0].get_paths()) == 6
    assert result.axes.get_aspect() == 1.0


def test_poincare_scatter_and_trajectory_render_nonblank_3d_artists():
    _, _, s1, s2, s3 = _field()
    scatter = render_poincare_scatter(s1, s2, s3, step=(2, 2))
    assert len(scatter.artists) == 2
    assert scatter.axes.name == "3d"
    trajectory = render_poincare_trajectory(
        np.cos(np.linspace(0, 2 * np.pi, 20)),
        np.sin(np.linspace(0, 2 * np.pi, 20)),
        np.zeros(20),
    )
    assert len(trajectory.artists) == 20


def test_surface_renderer_transposes_xy_field_for_matplotlib():
    x, y, s1, _, _ = _field()
    result = render_surface_3d(x, y, s1)
    assert result.axes.name == "3d"
    assert len(result.artists) == 1
