import asyncio
import math

from .brush import BrushWipe
from .path import PathZigZag
from .renderer import AnimationRender


def main():
    r = AnimationRender()

    # You might customize the wipe brush
    bw = BrushWipe()

    # You might create your own wipe path
    path_points = PathZigZag(
        size=math.floor(bw.width / 2),
        brush_deformation_factor=bw.deformation_factor,
        max_x=r.screen_size.width,
        max_y=r.screen_size.height,
    ).get_points_list()

    frame_rate = 0.006
    for idx, pp in enumerate(path_points):
        for bwp in bw.get_points(*pp.coord, pp.angle):
            r.schedule_draw(
                timeout=idx * frame_rate,
                p=bwp.coord,
                s='#',
                clean_after=0.03
            )

    asyncio.run(r.render_frames())


if __name__ == '__main__':
    main()
