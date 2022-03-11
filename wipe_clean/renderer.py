import asyncio
import heapq
import time
from typing import NamedTuple, List, Optional

from ._rich.control import ControlType, CONTROL_CODES_FORMAT
from ._rich.simple_console import SimpleConsole
from .screen import ScreenPoint


def clamp(minimum, v, maximum):
    return max(minimum, min(v, maximum))


def sleep(second: float):
    start = time.monotonic()
    while time.monotonic() - start < second:
        continue


class Render(SimpleConsole):

    @property
    def screen_size(self):
        return self.size

    def move_cursor_home(self):
        char_control = CONTROL_CODES_FORMAT[ControlType.HOME]()
        self.write(char_control)
        self.flush()

    def clear(self):
        char_control = CONTROL_CODES_FORMAT[ControlType.CLEAR]()
        self.write(char_control)
        self.flush()

    def draw_string_at(self, p: ScreenPoint, s: str, flush=True):

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

        char_control = CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](x, y)
        self.write(char_control + s)

        if flush:
            self.flush()


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
            self.schedule_draw(timeout + clean_after, p, ' ', clean_after=None)

    @staticmethod
    def _process_frames(frames: List[TimedDrawStruct]):
        """
        Return a time-index chuck of `TimedDrawStruct`.

        Assuming `frames` are sorted (by time).
        (e.g. `self._scheduled` is always sorted)
        """
        if len(frames) == 0:
            return []
        if len(frames) == 1:
            return [frames]

        # The chuck, they should have the same `time_s` values
        chuck_by_time: List[
            List[AnimationRender.TimedDrawStruct]
        ] = []

        def _insert(chuck: List[AnimationRender.TimedDrawStruct]):
            if not chuck:
                return
            chuck_by_time.append(chuck)

        slow, fast = 0, 1
        while True:
            if fast == len(frames):
                _insert(frames[slow:fast])
                break
            if frames[fast].time_s != frames[slow].time_s:
                _insert(frames[slow:fast])
                slow = fast
            fast += 1

        return chuck_by_time

    async def render_frames(self, min_frame_delay=0.006):

        # NOTED: We assume all frames are already scheduled i.e. `self._scheduled` is fixed

        if len(self._scheduled) == 0:
            return

        chuck_by_time = self._process_frames(
            heapq.nsmallest(len(self._scheduled), self._scheduled)
        )

        start_time = 0
        for chuck in chuck_by_time:
            delay = chuck[0].time_s - start_time

            if delay > min_frame_delay:
                sleep(delay)

            start_time = time.monotonic()
            for st in chuck:
                self.draw_string_at(st.point, st.char, flush=False)
            self.flush()
            elapse = time.monotonic() - start_time

            start_time = chuck[0].time_s + elapse
