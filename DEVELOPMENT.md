# Development


## Develop locally

Dependencies:

- [python-poetry](https://python-poetry.org/)

Setup:

```bash
poetry install
```

Run local tests:

```
poetry run pytest
```

## Testing on Docker


### Interactive shell

<table>
<tr><td>bash</td><td>Powershell</td></tr>
<tr>
<td>

```bash
docker run \
  -v $(pwd)/dist:/pkgdist:ro \
  -w /pkgdist \
  --name test_wipe_clean \
  --rm -it \ 
  python:3-alpine \
  /bin/sh
```

</td>
<td>

```powershell
docker run `
  -v $pwd/dist:/pkgdist:ro `
  -w /pkgdist `
  --name test_wipe_clean `
  --rm -it `
  python:3-alpine `
  /bin/sh
```

</td>
</tr>
</table>

Then run, e.g.

```bash
pip install wipe-clean-0.1.4.tar.gz

wipe-clean
```



## Development Notes

### APIs

Some interesting APIs from `rich`

- `Control.move(x, y)`
- `Control.move_to(x, y)`
- `Segment(text, style, control)`
- `LiveRender`


### TODOs

#### 1. ✅ How to use a `rich.control`

<details><summary>Expand</summary>

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

</details>

#### 2. ✅ Make 0-dependency

#### 3. Make compatible with python 2.7

Combining with #2, this will benefit many Linux distributions.

#### 4. (Doc) asciinema

#### 5. ✅ Documentation on `Path` and `Brush` usages for customization/extension

#### 6. ✅ Config from command-line

<details><summary>Expand</summary>

e.g. `speed`, animation profiles

</details>

#### 7. ✅ Animation scheduling revamp

<details><summary>Expand</summary>

- Frame-based scheduler (instead of time-based). This allows more accurate control on frame timer,
  which may help solve the Windows timer issue.

</details>
