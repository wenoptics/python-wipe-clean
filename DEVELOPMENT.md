# Development notes


## APIs

Some interesting APIs from `rich`

- `Control.move(x, y)`
- `Control.move_to(x, y)`
- `Segment(text, style, control)`
- `LiveRender`


## Objectives

### 1. How to use a `rich.control`

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
