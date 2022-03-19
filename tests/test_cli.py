import contextlib
from io import StringIO

import pytest

from wipe_clean.main import cli


def test_cli_help():
    import pytest
    from wipe_clean.main import cli

    stdout_capture = StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        with pytest.raises(SystemExit):
            cli('--help')

    assert stdout_capture.getvalue().strip()


@pytest.mark.skip
def test_simple():
    # Noted this is more like a dummy test run
    cli()
    cli('--frame-interval=0.005')


if __name__ == '__main__':
    cli('--frame-interval=0.003')
