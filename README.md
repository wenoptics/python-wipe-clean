# Wipe Clean

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wipe-clean?logo=python)

[![PyPI](https://img.shields.io/pypi/v/wipe-clean?logo=pypi)](https://pypi.org/project/wipe-clean/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/wipe-clean)](https://pypi.org/project/wipe-clean/)
[![PyPI - Status](https://img.shields.io/pypi/status/wipe-clean)](https://pypi.org/project/wipe-clean/)

[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com/wenoptics/python-wipe-clean)
[![Mac OS](https://img.shields.io/badge/MacOS--9cf?logo=Apple&style=social)](https://github.com/wenoptics/python-wipe-clean)
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)](https://github.com/wenoptics/python-wipe-clean)

---

Clear your terminal in a ritual way. Works on Windows, Linux and macOS.

```bash
pip install wipe-clean
```

![demo](https://github.com/wenoptics/python-wipe-clean/blob/master/doc/terminal.gif?raw=true)


> `wipe-clean` requires Python 3.6.1 and above. Note that Python 3.6.0 is
 not supported due to lack of `NamedTuples` typing.

> `wipe-clean` is moving to pursue **0-dependency**, see the [Roadmap](#roadmap).


## Usages

Just:

```bash
wipe-clean
```

## Advanced Usages

### 1. Use API

```python
from wipe_clean.main import cli as wc_cli

wc_cli()
```

### 2. Customization

It's possible to design your own brush shape and animation!

#### Example Brush

To create a new brush type, just implement the `Brush` interface.

```python
from wipe_clean.brush import Brush, ScreenPointDrawing, ScreenPoint as P

class Wipe2x2(Brush):
    def get_points(self, x, y, angle) -> List[ScreenPointDrawing]:
        return [
            ScreenPointDrawing(P(x    , y    ), '#'),
            ScreenPointDrawing(P(x + 1, y    ), '#'),
            ScreenPointDrawing(P(x    , y + 1), '#'),
            ScreenPointDrawing(P(x + 1, y + 1), '#'),
        ]
```

This will define a brush like this:

```text
##
##
```

#### Example Path

Similarly, you can implement the `Path` interface.

```python
import math
from wipe_clean.path import Path, PathPoint, ScreenPoint as P

class MySimplePath(Path):
    def get_points(self) -> Iterable[PathPoint]:
        return [
            PathPoint(P(10, 10), math.radians(45)),
            PathPoint(P(20, 5), math.radians(0)),
            PathPoint(P(40, 20), math.radians(90)),
        ]
```


## Roadmap

See [`DEVELOPMENT.md`](./DEVELOPMENT.md)


## Related Projects

- [`JeanJouliaCode/wipeclean`](https://github.com/JeanJouliaCode/wipeClean) - JavaScript version

  _The first brush type (`BrushWipe`) and path animations (`PathZigZag`, `PathRectEdge`) are direct ports
  of `JeanJouliaCode/wipeclean`. Credits go to JeanJouliaCode!_

- [`Textualize/rich`](https://github.com/Textualize/rich) - _Inspiring textual UI library_
