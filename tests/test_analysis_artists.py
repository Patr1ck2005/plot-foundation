from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from plot_foundation import (
    plot_field_regime_splits,
    plot_lineshape_comparison,
)


def test_lineshape_comparison_draws_on_caller_axes():
    x = np.linspace(-1.0, 1.0, 11)
    first = SimpleNamespace(x_fit=x, y_fit=x**2, model="lorentzian")
    second = SimpleNamespace(x_fit=x, y_fit=x**2 + 0.1, model="fano")
    fig, ax = plt.subplots()
    try:
        result = plot_lineshape_comparison(ax, x, x**2, first, second, best_result=first)
        assert result is ax
        assert len(ax.lines) == 2
        assert len(ax.collections) == 1
        assert "lorentzian" in ax.get_title()
    finally:
        plt.close(fig)


def test_field_regime_segments_draw_on_caller_axes():
    splits = {
        "phi0": [np.array([[0.0, 0.0], [1.0, 1.0]])],
        "phi90": [np.array([[0.0, 1.0], [1.0, 0.0]])],
        "uncertain": [],
    }
    fig, ax = plt.subplots()
    try:
        assert plot_field_regime_splits(ax, splits) is ax
        assert len(ax.lines) == 2
    finally:
        plt.close(fig)
