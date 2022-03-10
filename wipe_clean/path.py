import math
from abc import ABC, abstractmethod
from typing import NamedTuple, Iterable, List, Tuple

from .screen import ScreenPoint


class PathPoint(NamedTuple):
    coord: ScreenPoint
    angle: float


class Path(ABC):
    @abstractmethod
    def get_points(self) -> Iterable[PathPoint]:
        pass

    def get_points_list(self):
        return list(self.get_points())


class PathCircle(Path):
    angle_step = math.radians(5)

    def __init__(self, radius, start, end, deformation_factor=3):
        self.radius = radius
        self.start = start
        self.end = end
        self.deformation_factor = deformation_factor

    def get_points(self) -> Iterable[PathPoint]:
        points = []
        angle = self.start
        while angle < self.end:
            points.append(PathPoint(
                ScreenPoint(
                    x=math.cos(angle) * self.radius * self.deformation_factor,
                    y=math.sin(angle) * self.radius,
                ),
                angle
            ))
            angle += self.angle_step
        return points


class PathLine(Path):
    def __init__(self, start: ScreenPoint, end: ScreenPoint):
        self.start = start
        self.end = end

    def get_points(self) -> Iterable[PathPoint]:
        points = []
        y_step = (self.end.y - self.start.y) / abs(self.end.x - self.start.x)
        x_dir = 1 if self.end.x > self.start.x else -1
        angle = -math.atan((self.end.y - self.start.x) / self.start.y - self.end.y)

        for step in range(int(abs(self.end.x - self.start.x))):
            points.append(PathPoint(
                ScreenPoint(
                    x=step * x_dir + self.start.x,
                    y=step * y_step + self.start.y
                ),
                angle
            ))
        return points


class PathZigZag(Path):

    def __init__(self, size, brush_deformation_factor, max_x, max_y):
        self.size = size
        self.brush_deformation_factor = brush_deformation_factor
        self.max_x = max_x
        self.max_y = max_y

    def _get_key_points(self) -> List[Tuple[ScreenPoint, ScreenPoint]]:
        half_d = (self.size * self.brush_deformation_factor) / 2

        points = []
        step = 0
        while (self.size / 2) * 3 + (step - 1) * self.size < self.max_y:
            points.append((
                ScreenPoint(
                    x=half_d * 2,
                    y=(self.size / 2) * 2 + step * self.size
                ),
                ScreenPoint(
                    x=self.max_x - half_d * 2,
                    y=(self.size / 2) * 1 + step * self.size
                )
            ))
            points.append((
                ScreenPoint(
                    x=self.max_x - half_d * 2,
                    y=(self.size / 2) * 3 + step * self.size
                ),
                ScreenPoint(
                    x=half_d * 2,
                    y=(self.size / 2) * 2 + step * self.size
                ),
            ))
            step += 1

        return points

    def get_points(self) -> Iterable[PathPoint]:
        # Get half circle path
        circle_points_left = PathCircle(
            self.size // 2,
            math.pi / 2,
            (math.pi * 3) / 2,
        ).get_points_list()
        circle_points_left.reverse()

        circle_points_right = PathCircle(
            self.size // 2,
            (math.pi * 3) / 2,
            (math.pi * 5) / 2,
        ).get_points_list()

        key_points = self._get_key_points()

        points = []
        for step in range(len(key_points)):
            p0, p1 = key_points[step]

            line = PathLine(p0, p1).get_points_list()

            turn = circle_points_right if step % 2 == 0 else circle_points_left
            turn = [PathPoint(ScreenPoint(
                p.coord.x + p1.x,
                p.coord.y + p1.y + self.size / 2,
            ), p.angle) for p in turn]

            points.extend(line)
            points.extend(turn)

        return points


class PathRectEdge(Path):
    def __init__(self, start: PathPoint, size, brush_deformation_factor, max_x, max_y):
        self.start = start
        self.size = size
        self.brush_deformation_factor = brush_deformation_factor
        self.max_x = max_x
        self.max_y = max_y

    def get_points(self) -> Iterable[PathPoint]:
        margin_v = self.size / 2
        margin_h = self.size * self.brush_deformation_factor / 2
        start = ScreenPoint(self.start.coord.x, self.max_y - margin_v)

        points = []
        for x in range(int(start.x), -2, -1):
            points.append(PathPoint(ScreenPoint(
                x,
                self.max_y - margin_v + 1
            ), math.pi / 2))

        angle_points = PathCircle(self.size / 2, 0, math.pi / 2).get_points_list()
        angle_points = [PathPoint(ScreenPoint(
            p.coord.x,
            p.coord.y + self.max_y - margin_v * 2
        ), p.angle) for p in angle_points]
        points.extend(angle_points[::-1])

        for y in range(int(self.max_y - margin_v - 3), -1, -1):
            points.append(PathPoint(ScreenPoint(
                margin_h - 1,
                y
            ), math.pi))

        angle_points = PathCircle(self.size / 2, math.pi, math.pi * 3 / 2).get_points_list()
        angle_points = [PathPoint(ScreenPoint(
            p.coord.x + margin_h * 2,
            p.coord.y
        ), p.angle) for p in angle_points]
        points.extend(angle_points[::-1])

        for x in range(int(margin_h + 3), self.max_x, 1):
            points.append(PathPoint(ScreenPoint(
                x,
                margin_v - 1
            ), math.pi / 2))

        angle_points = PathCircle(self.size / 2, math.pi, math.pi * 3 / 2).get_points_list()
        angle_points = [PathPoint(ScreenPoint(
            p.coord.x + self.max_x,
            p.coord.y + margin_v * 2
        ), p.angle) for p in angle_points]
        points.extend(angle_points[::-1])

        for y in range(int(margin_v + 3), self.max_y, 1):
            points.append(PathPoint(ScreenPoint(
                self.max_x - margin_h,
                y
            ), math.pi))

        angle_points = PathCircle(self.size / 2, math.pi * 3 / 2, math.pi * 4 / 2).get_points_list()
        angle_points = [PathPoint(ScreenPoint(
            p.coord.x + self.max_x - margin_h * 2,
            p.coord.y + self.max_y
        ), p.angle) for p in angle_points]
        points.extend(angle_points[::-1])

        for x in range(int(self.max_x - margin_h - 3), self.max_x, -1):
            points.append(PathPoint(ScreenPoint(
                x,
                self.max_y - margin_v
            ), math.pi / 2))

        return points
