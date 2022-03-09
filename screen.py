from typing import NamedTuple


class ScreenPoint(NamedTuple):
    x: int
    y: int


class ScreenPointDrawing(NamedTuple):
    coord: ScreenPoint
    char: str