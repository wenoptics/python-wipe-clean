import math

from rich.console import Console
from rich.control import Control

from brush import BrushWipe
from path import PathZigZag
from screen import ScreenPoint


class Render:
    def __init__(self, console: Console = None):
        self.console = console or Console()

    @property
    def screen_size(self):
        return self.console.size

    def draw_string_at(self, p: ScreenPoint, s: str):
        def clamp(minimum, v, maximum):
            return max(minimum, min(v, maximum))

        # if p.x > self.screen_size.width - 1:
        #     return
        # if p.y > self.screen_size.height - 1:
        #     return
        # if p.x < 0:
        #     return
        # if p.y < 0:
        #     return

        x = int(clamp(0, p.x, self.screen_size.width - 2))
        y = int(clamp(0, p.y, self.screen_size.height - 2))

        self.console.control(Control.move_to(x, y))
        # self.console.print(s)
        self.console.out(s)


if __name__ == '__main__':

    r = Render()
    bw = BrushWipe()

    path_points = PathZigZag(
        size=math.floor(bw.width / 2),
        brush_deformation_factor=bw.deformation_factor,
        max_x=r.screen_size.width,
        max_y=r.screen_size.height,
    ).get_points_list()

    for pp in path_points:
        r.draw_string_at(pp.coord, '#')

    #
    # p_list = bw.get_points(10, 5, math.radians(90))
    #
    # for _p in p_list:
    #     r.draw_string_at(_p.coord, _p.char)

