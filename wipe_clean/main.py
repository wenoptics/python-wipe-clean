import asyncio

from .brush import BrushWipe
from .path import PathZigZag, PathRectEdge
from .renderer import AnimationRender


def main():
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
    r.move_cursor_home()
    r.clear()


if __name__ == '__main__':
    main()
