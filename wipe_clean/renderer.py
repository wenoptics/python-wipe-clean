import asyncio
import heapq
import platform
import time
from functools import cache
from typing import NamedTuple, List, Optional, Dict, Union, Tuple

from ._rich.control import ControlType, CONTROL_CODES_FORMAT
from ._rich.simple_console import SimpleConsole
from .screen import ScreenPoint

WINDOWS = platform.system() == 'Windows'


def clamp(minimum, v, maximum):
    return max(minimum, min(v, maximum))


async def sleep(second: float):
    if second <= 0:
        return
    if second > 0.1:
        return await asyncio.sleep(second)
    start = time.perf_counter()
    while time.perf_counter() - start < second:
        continue


class Render(SimpleConsole):

    @property
    @cache
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

    def string_at(self, p: Union[Tuple, ScreenPoint], s: str) -> str:
        """Use the terminal control character to position a string"""

        if not isinstance(p, ScreenPoint):
            p = ScreenPoint(*p)

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
        return char_control + s

    def draw_string_at(self, p: Union[Tuple, ScreenPoint], s: str, flush=True):
        self.write(self.string_at(p, s))

        if flush:
            self.flush()


class AnimationRender(Render):
    CLEAR_CHAR = ' '

    class TimedDrawStruct(NamedTuple):
        frame_idx: int
        point: ScreenPoint
        char: str

    class TimedDrawFullFrame(NamedTuple):
        frame_idx: int
        buffer: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will be maintained sorted (priority queue)
        self._scheduled: List[AnimationRender.TimedDrawStruct] = []
        self._evt_stop = asyncio.Event()

    def schedule_draw(
            self,
            frame: int, p: ScreenPoint, s: str,
            clean_after: Optional[int] = None
    ):
        heapq.heappush(self._scheduled, AnimationRender.TimedDrawStruct(frame, p, s))

        if clean_after is not None:
            self.schedule_draw(frame + clean_after, p, self.CLEAR_CHAR, clean_after=None)

    def _process_frames(self, frames: List[TimedDrawStruct]) -> List[TimedDrawFullFrame]:
        """
        Return a time-indexed full frame. The potential issue of this implementation is that,
        The full frame string will be fixed during such `process`-time, so if terminal got resized this,
        the drawing will be messed up.

        Assuming `frames` are already sorted (by time).
        """
        if len(frames) == 0:
            return []

        frame_list: List[AnimationRender.TimedDrawFullFrame] = []

        def _insert(chuck: List[AnimationRender.TimedDrawStruct]):
            if not chuck:
                return

            frame_idx = chuck[0].frame_idx
            frame: Dict[ScreenPoint, str] = {}

            for tds in chuck:
                if tds.frame_idx != frame_idx:
                    raise RuntimeError('All the `TimedDrawStruct`s must have the same frame index')

                same_pos = frame.get(tds.point)
                if tds.char == self.CLEAR_CHAR and same_pos and same_pos != self.CLEAR_CHAR:
                    # If the (x, y) is already scheduled with a non-clear-char, don't put the clear-char here.
                    continue
                frame[tds.point] = tds.char

            frame_str = ''.join([self.string_at(p, frame[p]) for p in frame])
            frame_list.append(AnimationRender.TimedDrawFullFrame(frame_idx, frame_str))

        # Chunk all the frames in O(n) time
        slow, fast = 0, 1
        while True:
            if fast == len(frames):
                _insert(frames[slow:fast])
                break
            if frames[fast].frame_idx != frames[slow].frame_idx:
                _insert(frames[slow:fast])
                slow = fast
            fast += 1

        return frame_list

    async def render_frames(self, frame_interval_s=0.005, min_sleep_delay=0):

        # NOTED: We assume all frames are already scheduled i.e. `self._scheduled` is fixed

        if len(self._scheduled) == 0:
            return

        full_frame_list = self._process_frames(
            # Pop all the items (sorted)
            heapq.nsmallest(len(self._scheduled), self._scheduled)
        )

        current_frame = 0
        for frame in full_frame_list:
            empty_frames = frame.frame_idx - current_frame

            if empty_frames > 0:
                sleep_time = frame_interval_s * empty_frames
                if sleep_time > min_sleep_delay:
                    await sleep(sleep_time)

            self.write(frame.buffer)
            self.flush()

            current_frame = frame.frame_idx
