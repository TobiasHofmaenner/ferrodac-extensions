# Moving-average smoothing

## What it computes

For a measured 1-D spectrum `y(x)`, the **moving average** replaces each point with the
mean of a window of `w` neighbouring samples:

$$ \tilde{y}_i = \frac{1}{w}\sum_{k=-(w-1)/2}^{(w-1)/2} y_{i+k} $$

equivalently a convolution of `y` with a normalised boxcar kernel of width `w`.

## Why it's useful

It's the simplest low-pass filter: it suppresses high-frequency measurement noise so a
peak's shape and position are easier to read (and easier for a downstream processor like
**window-integral** to integrate). Increase `w` for more smoothing.

## Assumptions & caveats

- A boxcar broadens and flattens sharp peaks — keep `w` well below a peak's width, or the
  peak height/resolution suffers. For peak-preserving smoothing use Savitzky–Golay instead.
- Edges: with a `same`-length convolution the first/last `w/2` points are biased by the
  implicit zero-padding; ignore the extreme edges if it matters.
- The output is a new spectrum on the **same x-axis** — route it back onto a Spectrum or
  Waterfall panel to compare with the raw trace.

## References

- Smith, S. W. *The Scientist and Engineer's Guide to Digital Signal Processing*, ch. 15
  (Moving Average Filters).
- For peak-preserving smoothing: Savitzky, A.; Golay, M. J. E. *Anal. Chem.* **36** (1964) 1627.
