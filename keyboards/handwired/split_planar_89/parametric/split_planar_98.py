from pathlib import Path
from time import perf_counter
import cadquery as cq

from iso_keys import *
from iso_matrix import build_keyboard_matrix

cq_objects = []
pc_0 = perf_counter()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def construct_keyboard():
    c = cq.Workplane("XY")
    last_row = None
    last_key = None
    for row in build_keyboard_matrix():

        print("")
        is_first_key_in_row = True
        for key in row:

            if is_first_key_in_row and last_row is not None:
                key.key_base.set_position_relative_to(last_row[0].key_base, Direction.TOP)
            elif last_key is not None:
                key.key_base.set_position_relative_to(last_key.key_base, Direction.RIGHT)
            is_first_key_in_row = False
            last_key = key

            cq_objects.append(c.box(key.cap.width, key.cap.depth, key.cap.thickness).translate(tuple(key.key_base.position)))
            print("{}".format(key.key_base.position))
        last_row = row


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pc_1 = perf_counter()
    print("elapsed {:.3f}s for loading".format(pc_1 - pc_0))
    construct_keyboard()
    pc_2 = perf_counter()
    print("elapsed {:.3f}s for construction".format(pc_2 - pc_1))

    if cliargs.export:
        u = cq.Workplane("XY")
        for c in cq_objects:
            u = u.union(c)
        pc_3 = perf_counter()
        print("elapsed {:.3f}s for unifying objects".format(pc_3 - pc_2))

        filename = Path("{}/{}".format(cliargs.path, cliargs.filename)).name
        print("exporting to: {}".format(filename))
        cq.exporters.export(u, filename)
        pc_4 = perf_counter()
        print("elapsed {:.3f}s for export".format(pc_4 - pc_3))
else:
    pc_1 = perf_counter()
    print("elapsed {:.3f}s for loading".format(pc_1 - pc_0))
    construct_keyboard()
    pc_2 = perf_counter()
    print("elapsed {:.3f}s for construction".format(pc_2 - pc_1))
    for o in cq_objects:
        show_object(o)
