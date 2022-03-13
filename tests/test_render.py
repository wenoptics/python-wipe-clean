from unittest.mock import patch, PropertyMock

from wipe_clean.renderer import Render
from wipe_clean._rich.simple_console import ConsoleDimensions


def test_rendering():

    with patch(f'{Render.__module__}.{Render.__name__}.screen_size', new_callable=PropertyMock) as mock_render:
        # Mock the screen size (e.g. CI won't have a determined screen size)
        mock_render.return_value = ConsoleDimensions(10, 10)

        r = Render()
        assert r.screen_size.width == r.screen_size.height == 10, 'Mocking should have effect'

        x, y = 2, 5
        buf = r.string_at((x, y), '#')
        assert buf == f"\x1b[{y+1};{x+1}H#"

        x, y = 2.2, 5.8
        buf = r.string_at((x, y), '#')
        assert buf == f"\x1b[{5+1};{2+1}H#"
