# ferroDAC extensions

Official, open extensions for [ferroDAC](https://github.com/TobiasHofmaenner/ferroDAC) —
device drivers, data **processors**, and display **widgets**. Science should be open, and
data-analysis code gets shared far too rarely; every extension here ships its **source**
(you can read exactly what it does) and, where it matters, a **white paper** explaining the
algorithm and citing the literature.

## Layout — a monorepo of extensions

Each top-level directory is **one extension**, with its own `ferrodac-extension.toml`
manifest:

```
ferrodac-extensions/
└── window-integral/            # one extension
    ├── ferrodac-extension.toml # what it provides + white papers + api version
    ├── window_integral/        # a normal importable Python package
    └── papers/                 # white papers (PDF / MD)
```

ferroDAC discovers extensions by scanning a cloned repo for `ferrodac-extension.toml`
files, lists what it finds, and lets you enable the ones you want (behind a "this runs
code on your machine" gate). A repo with a single manifest at its root is also valid —
one repo can be one extension or many.

## Extensions

| Extension | Kind | What it does |
|-----------|------|--------------|
| [`window-integral`](window-integral/) | processor | Integrate a spectrum over an m/z window → a scalar (a partial-pressure proxy). |
| [`smoother`](smoother/) | processor | Moving-average (boxcar) smoothing of a spectrum (trace → trace). |

## Writing your own

Subclass the bases from the stable SDK and register them:

```python
from ferrodac.plugin import Processor, Port, FLOAT, register_processor

@register_processor
class MyProcessor(Processor):
    kind = "my_processor"
    accepts = "trace"
    ...
```

**Only** import from `ferrodac.plugin` — it's the one surface promised to stay stable
(versioned by the manifest's `api` field). Datatypes are a small, closed, documented set
(`float`, `bool`, `trace`; `trace` is a 1-D labelled array, interoperable with
xarray/pint). See the [`window-integral`](window-integral/) extension as a template.

## License

MIT — see [LICENSE](LICENSE).
