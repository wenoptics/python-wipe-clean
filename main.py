import math
from abc import ABC, abstractmethod
from typing import NamedTuple, List

from rich.console import Console
from rich.control import Control

# console = Console()
# print(console.size)
# width, height = console.size


class ScreenPoint(NamedTuple):
    x: int
    y: int


class Render:
    def __init__(self, console: Console = None):
        self.console = console or Console()

    def draw_string_at(self, p: ScreenPoint, s: str):
        self.console.control(Control.move_to(int(p.x), int(p.y)))
        self.console.print(s)


class Brush(ABC):
    @abstractmethod
    def get_points(self, x, y, angle) -> List[ScreenPoint]:
        pass


class BrushWipe(Brush):
    width = 6
    deformation_factor = 2

    def get_points(self, x, y, angle) -> List[ScreenPoint]:
        """Return all the brush points"""

        half_width = self.width / 2
        opposite_angle = angle + math.pi

        ret = []
        for step in range(0, int(half_width * self.deformation_factor)):
            fac = half_width / (half_width * self.deformation_factor) * step

            new_x = x + math.cos(angle)          * fac * self.deformation_factor
            new_y = y + math.sin(angle)          * fac
            ret.append(ScreenPoint(new_x, new_y))

            new_x = x + math.cos(opposite_angle) * fac * self.deformation_factor
            new_y = y + math.sin(opposite_angle) * fac
            ret.append(ScreenPoint(new_x, new_y))

        return ret


if __name__ == '__main__':
    bw = BrushWipe()
    p_list = bw.get_points(10, 5, math.radians(90))
    r = Render()

    for _p in p_list:
        r.draw_string_at(_p, '#')

