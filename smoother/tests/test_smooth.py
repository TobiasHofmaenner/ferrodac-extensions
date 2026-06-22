"""The extension's own tests (run where ferrodac.plugin is installed)."""
import types

import numpy as np

from smoother.processors.smooth import MovingAverage


def test_moving_average_smooths_noise():
    p = MovingAverage("smooth1", "src", window=5, name="clean")
    x = np.linspace(0, 10, 200)
    rng = np.random.default_rng(0)
    noisy = np.sin(x) + 0.3 * rng.standard_normal(x.size)
    out = p.process(types.SimpleNamespace(x=x, y=noisy, x_label="x", x_unit="", y_unit=""))
    smooth = out["smooth/smooth1/clean"]
    # a trace out, same x, and lower point-to-point variance than the input
    assert len(smooth.x) == len(x)
    assert np.std(np.diff(smooth.y)) < np.std(np.diff(noisy))
    assert p.outputs()[0].dtype == "trace"
