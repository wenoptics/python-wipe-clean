import asyncio
import math
from typing import Optional

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tasks = asyncio.Queue(500)

    async def _draw_with_delay(self, timeout: float, p: ScreenPoint, s: str):
        await asyncio.sleep(timeout)
        self.draw_string_at(p, s)

    async def schedule_draw(
            self,
            timeout: float, p: ScreenPoint, s: str,
            clean_after: Optional[float] = None
    ):
        await self._tasks.put(
            asyncio.create_task(self._draw_with_delay(timeout, p, s))
        )

        if clean_after is not None:
            await self.schedule_draw(timeout + clean_after, p, ' ', None)

    async def gather(self):
        while True:
            coros = [
                self._tasks.get() for _ in range(self._tasks.qsize())
            ]
            if len(coros) == 0:
                await asyncio.sleep(0.1)
            else:
                await asyncio.gather(*coros)


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


    async def schedule():
        for idx, pp in enumerate(path_points):
            for bwp in bw.get_points(*pp.coord, pp.angle):
                await r.schedule_draw(idx * frame_rate, bwp.coord, '#', clean_after=0.1)

    async def run():
        await asyncio.gather(
            schedule(),
            r.gather(),
        )

    asyncio.run(run())

    #
    # p_list = bw.get_points(10, 5, math.radians(90))
    #
    # for _p in p_list:
    #     r.draw_string_at(_p.coord, _p.char)
