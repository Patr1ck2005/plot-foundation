from __future__ import annotations

import numpy as np
import pytest

from plot_foundation import (
    VectorFieldPlotSpec,
    VectorFieldStyle,
    render_vector_field,
)


def _field():
    x = np.asarray([-2.0, 0.0, 3.0])
    y = np.asarray([-4.0, -1.0, 0.0, 2.0, 5.0])
    X, Y = np.meshgrid(x, y, indexing="ij")
    return x, y, X + 1.0, Y - 0.5, X - Y


def test_non_square_x_first_field_and_asymmetric_sampling_are_preserved():
    x, y, u, v, color = _field()
    result = render_vector_field(
        VectorFieldPlotSpec(
            x=x, y=y, u=u, v=v, color_values=color, step=(2, 3),
            style=VectorFieldStyle(vmin=-5, vmax=5),
        )
    )
    quiver = result.artists[0]
    ii = np.asarray([0, 2])
    jj = np.asarray([0, 3])
    np.testing.assert_allclose(quiver.U, u[np.ix_(ii, jj)].ravel())
    np.testing.assert_allclose(quiver.V, v[np.ix_(ii, jj)].ravel())
    np.testing.assert_allclose(quiver.get_array(), color[np.ix_(ii, jj)].ravel())
    assert quiver.get_offsets().shape == (4, 2)


def test_normalized_director_is_invariant_under_phi_plus_pi():
    x = np.linspace(-1, 1, 4)
    y = np.linspace(-1, 1, 3)
    phi = np.linspace(-0.7, 0.8, 12).reshape(4, 3)
    first = render_vector_field(
        VectorFieldPlotSpec(
            x=x, y=y, u=np.cos(phi), v=np.sin(phi), glyph="director",
            style=VectorFieldStyle(normalize=True),
        )
    ).artists[0]
    second = render_vector_field(
        VectorFieldPlotSpec(
            x=x, y=y, u=np.cos(phi + np.pi), v=np.sin(phi + np.pi), glyph="director",
            style=VectorFieldStyle(normalize=True),
        )
    ).artists[0]
    np.testing.assert_allclose(np.abs(first.U), np.abs(second.U), atol=1e-12)
    np.testing.assert_allclose(np.abs(first.V), np.abs(second.V), atol=1e-12)


def test_zero_vectors_stay_zero_and_transposed_fields_are_rejected():
    x, y, u, v, _ = _field()
    zero = np.zeros_like(u)
    result = render_vector_field(
        VectorFieldPlotSpec(x=x, y=y, u=zero, v=zero, style=VectorFieldStyle(normalize=True))
    )
    assert np.count_nonzero(result.artists[0].U) == 0
    with pytest.raises(ValueError, match="x-first"):
        VectorFieldPlotSpec(x=x, y=y, u=u.T, v=v.T)
