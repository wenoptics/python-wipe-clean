import pytest

from wipe_clean.main import cli


@pytest.mark.skip
def test_simple():
    # Noted this is more like a dummy test run
    cli()
    cli('--frame-interval=0.005')


if __name__ == '__main__':
    cli('--frame-interval=0.003')
