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
    row_idx = 0
    for row in build_keyboard_matrix():
        print("row {}".format(row_idx))
        print(" col   x       y       z         key      ct   cr   cb   cl ")
        is_first_key_in_row = True
        col_idx = 0
        for key in row:
            if is_first_key_in_row and last_row is not None:
                key.key_base.set_position_relative_to(last_row[0].key_base, Direction.TOP)
            elif last_key is not None:
                key.key_base.set_position_relative_to(last_key.key_base, Direction.RIGHT)
            is_first_key_in_row = False
            last_key = key

            cq_objects.append(c.box(key.cap.width, key.cap.depth, key.cap.thickness).translate(tuple(key.key_base.position)))
            print("  {:2} [{:8.3f}{:8.3f}{:8.3f} ] {:7} {:4.2} {:4.2} {:4.2} {:4.2}"
                  .format(col_idx,
                          key.key_base.position[0], key.key_base.position[1], key.key_base.position[2],
                          key.name,
                          key.key_base.clearance_top,
                          key.key_base.clearance_right,
                          key.key_base.clearance_bottom,
                          key.key_base.clearance_left))
            col_idx = col_idx + 1
        last_row = row
        row_idx = row_idx + 1


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    construct_keyboard()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    if cliargs.export:
        u = cq.Workplane("XY")
        for c in cq_objects:
            u = u.union(c)
        pc_3 = perf_counter()
        print("{:.3f}s elapsed for unifying objects".format(pc_3 - pc_2))

        filename = Path("{}/{}".format(cliargs.path, cliargs.filename)).name
        print("exporting to: {}".format(filename))
        cq.exporters.export(u, filename)
        pc_4 = perf_counter()
        print("{:.3f}s elapsed for export".format(pc_4 - pc_3))
else:
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    construct_keyboard()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))
    for o in cq_objects:
        show_object(o)
