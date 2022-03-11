<div align="center">

# Wipe Clean

<a href="https://pypi.org/project/wipe-clean/">
  <img src="https://github.com/wenoptics/python-wipe-clean/blob/master/doc/logo.png?raw=true" alt="Logo" width="200" height="200">
</a>

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wipe-clean?logo=python)

[![PyPI](https://img.shields.io/pypi/v/wipe-clean?logo=pypi)](https://pypi.org/project/wipe-clean/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/wipe-clean)](https://pypi.org/project/wipe-clean/)
[![PyPI - Status](https://img.shields.io/pypi/status/wipe-clean)](https://pypi.org/project/wipe-clean/)

[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com/wenoptics/python-wipe-clean)
[![Mac OS](https://img.shields.io/badge/MacOS--9cf?logo=Apple&style=social)](https://github.com/wenoptics/python-wipe-clean)
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)](https://github.com/wenoptics/python-wipe-clean)

</div>

---

Clear your terminal in a _ritual_ way. Works on Windows, Linux and macOS. **0-dependency**.


![demo](https://github.com/wenoptics/python-wipe-clean/blob/master/doc/terminal.gif?raw=true)

Install with pip:

```bash
pip install wipe-clean
```

> `wipe-clean` currently requires Python 3.6.1 and above. Note that Python 3.6.0 is
 not supported due to lack of `NamedTuples` typing.


## Usages

Just:

```bash
wipe-clean
```

Use `-h, --help` to show all available options

```bash
wipe-clean -h
```

## Advanced usages

### 1. Use API

```python
from wipe_clean.main import cli as wc_cli

wc_cli()
# Or with arguments
wc_cli('--frame-interval=0.005', '--min-frame-delay=0')
```

### 2. Customization

It's possible to design your own brush shape and animation!

#### Example brush

To create a new brush type, implement the `Brush` interface, e.g.

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

#### Example path

Similarly, you can implement the `Path` interface to create a new brush path.

```python
import math
from wipe_clean.path import Path, PathPoint, ScreenPoint as P

class MySimplePath(Path):
    def get_points(self) -> Iterable[PathPoint]:
        return [
            PathPoint(P(10, 10), math.radians(45)),
            PathPoint(P(20,  5), math.radians( 0)),
            PathPoint(P(40, 20), math.radians(90)),
        ]
```


## Roadmap

See [`DEVELOPMENT.md`](./DEVELOPMENT.md)


## Related projects

- [`JeanJouliaCode/wipeclean`](https://github.com/JeanJouliaCode/wipeClean) - JavaScript version

  _The first brush type (`BrushWipe`) and path animations (`PathZigZag`, `PathRectEdge`) are direct ports
  of `JeanJouliaCode/wipeclean`. Credits go to JeanJouliaCode!_

- [`Textualize/rich`](https://github.com/Textualize/rich) - _An inspiring textual UI library_
