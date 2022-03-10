import asyncio
import heapq
import math
import time
from typing import Optional, NamedTuple, List

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

        x = int(clamp(0, p.x, self.screen_size.width - 1))
        y = int(clamp(0, p.y, self.screen_size.height - 2))

        self.console.control(Control.move_to(x, y))
        self.console.out(s, end='')


class AnimationRender(Render):

    class TimedDrawStruct(NamedTuple):
        time_s: float
        point: ScreenPoint
        char: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will be maintained sorted (priority queue)
        self._scheduled: List[AnimationRender.TimedDrawStruct] = []
        self._evt_stop = asyncio.Event()

    def schedule_draw(
            self,
            timeout: float, p: ScreenPoint, s: str,
            clean_after: Optional[float] = None
    ):
        heapq.heappush(self._scheduled, AnimationRender.TimedDrawStruct(timeout, p, s))

        if clean_after is not None:
            self.schedule_draw(timeout + clean_after, p, ' ', None)

    async def render_frames(self):
        _start_time = time.monotonic()

        while self._scheduled:
            st = heapq.heappop(self._scheduled)
            remaining_s = st.time_s - (time.monotonic() - _start_time)

            if remaining_s > 0:
                await asyncio.sleep(remaining_s)
            else:
                self.draw_string_at(st.point, st.char)


if __name__ == '__main__':

    r = AnimationRender()
    bw = BrushWipe()

    path_points = PathZigZag(
        size=math.floor(bw.width / 2),
        brush_deformation_factor=bw.deformation_factor,
        max_x=r.screen_size.width,
        max_y=r.screen_size.height,
    ).get_points_list()

    frame_rate = 0.006

    for idx, pp in enumerate(path_points):
        for bwp in bw.get_points(*pp.coord, pp.angle):
            r.schedule_draw(idx * frame_rate, bwp.coord, '#', clean_after=0.03)

    asyncio.run(r.render_frames())

    #
    # p_list = bw.get_points(10, 5, math.radians(90))
    #
    # for _p in p_list:
    #     r.draw_string_at(_p.coord, _p.char)
