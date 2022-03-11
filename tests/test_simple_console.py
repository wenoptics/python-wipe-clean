from wipe_clean.renderer import Render
from wipe_clean._rich.control import CONTROL_CODES_FORMAT, ControlType


def test_move_cursor():
    r = Render()

    x, y = 3, 4
    char_control = CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](x, y)
    r.write(char_control + '#')
    r.flush()


def test_move_cursor_batch():
    r = Render()

    r.write(CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](1, 1) + '#')
    r.write(CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](2, 2) + '#')
    r.write(CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](3, 3) + '#')
    r.write(CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](4, 4) + '#')
    r.write(CONTROL_CODES_FORMAT[ControlType.CURSOR_MOVE_TO](5, 5) + '#')
    r.flush()


if __name__ == '__main__':
    test_move_cursor_batch()
