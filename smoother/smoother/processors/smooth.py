"""A demo ferroDAC processor: moving-average (boxcar) smoothing of a spectrum.

A trace → trace processor: it consumes a 1-D spectrum and publishes a *smoothed*
spectrum, so you can route the result straight back onto a Spectrum or Waterfall panel
and see the effect. It pairs nicely with the window-integral processor in this repo
(integrate a smoothed peak) and shows the other common processor shape — trace in,
trace out — next to window-integral's trace → scalar.

Dependency-light (numpy only). See papers/smoothing.md for the white paper.
"""
from __future__ import annotations

import numpy as np

from ferrodac.plugin import TRACE, Port, Processor, Trace, register_processor


@register_processor
class MovingAverage(Processor):
    kind = "moving_average"             # registry key (unique across loaded plugins)
    label = "Moving-average smoother"   # human label (UI / /proc)
    accepts = "trace"                   # consumes a 1-D spectrum
    id_prefix = "smooth"                # output key prefix → "smooth/<id>/<name>"

    def __init__(self, pid: str, input_key: str, window: int = 5,
                 name: str = "smoothed", unit: str = ""):
        super().__init__(pid, input_key)
        self.window = max(1, int(window))   # smoothing width, in samples
        self.name, self.unit = name, unit

    def outputs(self) -> list[Port]:
        return [Port(f"{self.id_prefix}/{self.id}/{self.name}", self.name, TRACE, self.unit)]

    def process(self, value) -> dict:
        y = np.asarray(value.y, dtype=float)
        w = min(self.window, len(y)) or 1
        if w > 1:
            kernel = np.ones(w) / w
            y = np.convolve(y, kernel, mode="same")     # boxcar moving average
        out = Trace(x=np.asarray(value.x), y=y,
                    x_label=getattr(value, "x_label", "x"),
                    x_unit=getattr(value, "x_unit", ""),
                    y_label=self.name,
                    y_unit=self.unit or getattr(value, "y_unit", ""))
        return {f"{self.id_prefix}/{self.id}/{self.name}": out}

    def state(self) -> dict:
        return {"window": self.window, "name": self.name, "unit": self.unit}
