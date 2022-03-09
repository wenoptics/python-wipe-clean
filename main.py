from rich.console import Console
from rich.control import Control

r = Console()
print(r.size)

r.control(Control.move_to(2, 3))
r.print('123')

r.control(Control.move_to(4, 3))
r.print('456')
