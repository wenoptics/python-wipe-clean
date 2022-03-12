import asyncio
import random
import sys

from .fun import all_art
from .brush import BrushWipe
from .path import PathZigZag, PathRectEdge
from .renderer import AnimationRender


def main(
        frame_interval_s=0.003,
        clean_after=None,
        min_frame_delay=0
):
    if clean_after is None:
        clean_after = 1

    r = AnimationRender()

    # You might customize the wipe brush
    bw = BrushWipe()

    common_brush_cfg = dict(
        size=bw.width,
        brush_deformation_factor=bw.deformation_factor,
        max_x=r.screen_size.width,
        max_y=r.screen_size.height,
    )

    # You might create your own wipe path
    path_points = PathZigZag(**common_brush_cfg).get_points_list()
    path_points += PathRectEdge(path_points[-1], **common_brush_cfg).get_points_list()

    for idx, pp in enumerate(path_points):
        for bwp in bw.get_points(*pp.coord, pp.angle):
            r.schedule_draw(
                frame=idx,
                p=bwp.coord,
                s=bwp.char,
                clean_after=clean_after
            )

    try:
        asyncio.run(r.render_frames(frame_interval_s, min_frame_delay))
    except KeyboardInterrupt:
        pass

    r.clear()
    r.move_cursor_home()


def cli(*args):
    import argparse
    from argparse import RawTextHelpFormatter

    text = """
    wipe-clean - Clean your terminal in a ritual way
    """

    default = {
        'f': 0.003,
        'c': 1,
        'm': 0
    }

    parser = argparse.ArgumentParser(description=random.choice(all_art) + text, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--frame-interval', default=default['f'],
                        type=float, help='Frame interval (in second)')
    parser.add_argument('-c', '--clean-after', default=default['c'],
                        type=float, help='Clean drawn after number of frame(s)')
    parser.add_argument('-m', '--min-frame-delay', default=default['m'],
                        type=float, help='Minimum frame delay (in second). A delay will only be will be'
                                         ' scheduled when frame interval is larger than this value.'
                                         ' This may help solve the inaccurate sleep on Windows.')

    parsed_args = parser.parse_args(args)
    main(
        frame_interval_s=parsed_args.frame_interval,
        clean_after=parsed_args.clean_after,
        min_frame_delay=parsed_args.min_frame_delay
    )


def _outer_cli():
    sys.exit(
        cli(*sys.argv[1:])
    )


if __name__ == '__main__':
    _outer_cli()
