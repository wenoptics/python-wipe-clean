from wipe_clean.main import cli


def test_simple():
    cli()
    cli('--frame-interval=0.005')


if __name__ == '__main__':
    cli('--frame-interval=0.005', '--min-frame-delay=0.03')
