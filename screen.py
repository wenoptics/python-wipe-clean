from typing import NamedTuple


class ScreenPoint(NamedTuple):
    x: float
    y: float


class ScreenPointDrawing(NamedTuple):
    coord: ScreenPoint
    char: str
