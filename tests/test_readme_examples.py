import contextlib
from io import StringIO
from typing import List, Iterable

EXTRACTION_PATTERN = r'# Example extraction ---{' \
                     r'(.*?)' \
                     r'#\s*}--- End of example extraction'


def test_cli_usage():
    stdout_capture = StringIO()
    with contextlib.redirect_stdout(stdout_capture):

        # Example extraction ---{
        from wipe_clean.main import cli as wc_cli

        wc_cli()
        # Or with arguments
        wc_cli('--frame-interval=0.005', '--min-frame-delay=0')
        # }--- End of example extraction

    assert stdout_capture.getvalue()


def test_example_brush():
    # Example extraction ---{
    from wipe_clean.brush import Brush, ScreenPointDrawing, ScreenPoint as P

    class Wipe2x2(Brush):
        def get_points(self, x, y, angle) -> List[ScreenPointDrawing]:
            return [
                ScreenPointDrawing(P(x    , y    ), '#'),  # noqa: E202,E203
                ScreenPointDrawing(P(x + 1, y    ), '#'),  # noqa: E202,E203
                ScreenPointDrawing(P(x    , y + 1), '#'),  # noqa: E202,E203
                ScreenPointDrawing(P(x + 1, y + 1), '#'),
            ]
    # }--- End of example extraction

    p_list = Wipe2x2().get_points(0, 0, 0)
    assert p_list[0].coord.x == 0
    assert p_list[0].coord.y == 0
    assert p_list[0].char == '#'


def test_example_path():
    # Example extraction ---{
    import math
    from wipe_clean.path import Path, PathPoint, ScreenPoint as P

    class MySimplePath(Path):
        def get_points(self) -> Iterable[PathPoint]:
            return [
                PathPoint(P(10, 10), math.radians(45)),
                PathPoint(P(20,  5), math.radians(0)),
                PathPoint(P(40, 20), math.radians(90)),
            ]
    # }--- End of example extraction

    p_list = MySimplePath().get_points_list()
    assert p_list[1].coord.x == 20
    assert p_list[1].coord.y == 5
    assert p_list[1].angle == 0
