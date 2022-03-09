import math

from rich.console import Console
from rich.control import Control

from brush import BrushWipe
from screen import ScreenPoint


class Render:
    def __init__(self, console: Console = None):
        self.console = console or Console()

    def draw_string_at(self, p: ScreenPoint, s: str):
        self.console.control(Control.move_to(int(p.x), int(p.y)))
        self.console.print(s)


if __name__ == '__main__':
    bw = BrushWipe()
    p_list = bw.get_points(10, 5, math.radians(90))
    r = Render()

    for _p in p_list:
        r.draw_string_at(_p.coord, _p.char)

