import math
from abc import ABC, abstractmethod
from typing import List

from .screen import ScreenPoint, ScreenPointDrawing


class Brush(ABC):
    """
    Brush base class

    You may implement your own brush style.
    """

    @abstractmethod
    def get_points(self, x, y, angle) -> List[ScreenPointDrawing]:
        """Return all the brush points"""
        pass


class BrushWipe(Brush):
    width = 6
    deformation_factor = 2

    def get_points(self, x, y, angle) -> List[ScreenPointDrawing]:
        """Return all the brush points"""

        half_width = self.width / 2
        opposite_angle = angle + math.pi

        ret = []
        for step in range(0, int(half_width * self.deformation_factor)):
            fac = half_width / (half_width * self.deformation_factor) * step
            p = ScreenPoint(
                x + math.cos(angle)          * fac * self.deformation_factor,  # noqa: E221
                y + math.sin(angle)          * fac                             # noqa: E221
            )
            ret.append(ScreenPointDrawing(p, '#'))

            p = ScreenPoint(
                x + math.cos(opposite_angle) * fac * self.deformation_factor,
                y + math.sin(opposite_angle) * fac
            )
            ret.append(ScreenPointDrawing(p, '#'))

        return ret
