from wipe_clean.main import cli


def test_simple():
    cli()
    cli('-f=0.005')


if __name__ == '__main__':
    cli('-f=0.005', '-m=0.03')
