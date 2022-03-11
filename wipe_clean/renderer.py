import asyncio
import heapq
import time
from typing import NamedTuple, List, Optional

from ._rich.control import ControlType, CONTROL_CODES_FORMAT
from ._rich.simple_console import SimpleConsole
from .screen import ScreenPoint


def clamp(minimum, v, maximum):
    return max(minimum, min(v, maximum))


class Render(SimpleConsole):

    @property
    def screen_size(self):
        return self.size

    def move_cursor_home(self):
        char_control = CONTROL_CODES_FORMAT[ControlType.HOME]()
        self.write(char_control)

    def clear(self):
        char_control = CONTROL_CODES_FORMAT[ControlType.CLEAR]()
        self.write(char_control)

    def draw_string_at(self, p: ScreenPoint, s: str):
        def clamp(minimum, v, maximum):
            return max(minimum, min(v, maximum))

        # if p.x > self.screen_size.width - 1:
        #     return
        # if p.y > self.screen_size.height - 2:
        #     return
        # if p.x < 0:
        #     return
        # if p.y < 0:
        #     return
        # x = int(p.x)
        # y = int(p.y)

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
