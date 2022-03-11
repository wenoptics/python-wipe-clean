# Development notes


## APIs

Some interesting APIs from `rich`

- `Control.move(x, y)`
- `Control.move_to(x, y)`
- `Segment(text, style, control)`
- `LiveRender`


## TODOs

### 1. ✅ How to use a `rich.control`

We can use `Console.control()` to insert any controls.

e.g.
```python
from rich.console import Console
from rich.control import Control
r = Console()

r.control(Control.move_to(2, 3))
r.print('123')
  
r.control(Control.move_to(4, 3))
r.print('456')
```

```
 12456
```

### 2. Make 0-dependency (WIP)

### 3. Make compatible with python 2.7

Combining with #2, this will benefit many Linux distributions.

### 4. (Doc) asciinema

### 5. ✅ Documentation on `Path` and `Brush` usages for customization/extension

### 6. Config from command-line

e.g. `speed`, animation profiles

