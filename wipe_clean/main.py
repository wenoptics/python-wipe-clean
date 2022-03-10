import asyncio
import sys

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


def cli():

    import argparse
    from argparse import RawTextHelpFormatter

    art_ascii = """
     
                      g*R,
                    4`    *g
                 ,P    ,Rw  "w
               ,P    ,P   "W  "N
             gP    gP       ]M   $
           g"    g"       ,P ,P g"
         g`,   &`       gP gP g"
       g" "W   N      g" w" A`
     4`     "N   %, N`   ,P
    $          N,      gP
     "N          *g  g"
        N,        ,P"
          *g,,,,gP
     
    """

    art_extended = """
     
           █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
           █▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀▀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▄▓▓ ▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄▓▓▓▓ ▐▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓███████████████▓▓▓▓▓▓▀▀▀  ▓▓▓▓    ▀ ▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▒█████▓▓▓▓▓▓ ▐▓▌ ▓▓▓▓▌ ▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▒█▒▒░█▌▓▓▓▓▓▌ ▓▓ ▓▓▓▓  ▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▒█▒▒▒█▌▓▓▓▓▓▓▄▓▓▓▄▄▄▄▓▄▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▒█▒▒▒█▌▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▒█▒▒▒██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓▓▓▓█▒▒▒▒▒▒▒▒▒▒█▒▄███▀▀░░▀█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓▓▓██▀█▄░▒▒▒░░▄██▀▀░░▒▒▒▒▒▒▄█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌▓▓█▀░▒▒░▀▀███▀▀░░▒▒▒▒▒▒▒▒▒▒▒▀█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           █▌██░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▄█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
           ███░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
       ▄▄█▀▀░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
        █░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████▀▀▀▀▀▀█████
         █░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄█▀
         ▐█░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▄██▀
          ▐█░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▄██▀
           ▀█░▒░▄▄▄▄▄▄▄▄▄▄▄██▀▀▀
            ▀█▀▀
     
    """

    text = """
    wipe-clean - Clean your terminal in a ritual way
    """

    parser = argparse.ArgumentParser(description=art_extended + text, formatter_class=RawTextHelpFormatter)
    args = parser.parse_args()
    main()


if __name__ == '__main__':
    sys.exit(cli())
