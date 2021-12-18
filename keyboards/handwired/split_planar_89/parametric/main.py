from pathlib import Path
from time import perf_counter
from typing import Tuple

from utils import *
from iso_keys import *
from iso_matrix import build_keyboard_matrix
import cadquery as cq

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


objects = []  # type: List[Tuple[Key, cadquery.Workplane]]
pc_0 = perf_counter()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def construct_key_placement():
    last_row = None
    last_key = None
    row_idx = 0

    for row in build_keyboard_matrix():

        print("row {}".format(row_idx))
        print("  col x       y     z    key   unit clrto clrri clrbo clrle capwi  capde capth vis")
        is_first_key_in_row = True
        col_idx = 0

        for key in row:
            key.update()
            if is_first_key_in_row:
                if last_row is not None:
                    KeyUtils.set_position_relative_to(key.key_base, last_row[0].key_base, Direction.TOP)
                key.key_base.align_to_position(0, Direction.LEFT)
            elif last_key is not None:
                KeyUtils.set_position_relative_to(key.key_base, last_key.key_base, Direction.RIGHT)
            is_first_key_in_row = False
            last_key = key

            key.compute()
            objects.append((key, key.cad_objects.plane))
            objects.append((key, key.cad_objects.key_name))
            if key.key_base.is_visible:
                objects.append((key, key.cad_objects.key_cap))
            print("  {:2} |{:6.2f}{:6.2f}{:6.2f}|{:5} {:4.2f}|{:5.2f} {:5.2f} {:5.2f} {:5.2f}|{:6.2f} {:5.2f} {:5.2f}|{}"
                  .format(col_idx,
                          key.key_base.position[0], key.key_base.position[1], key.key_base.position[2],
                          key.name,
                          key.key_base.unit_width_factor,
                          key.key_base.clearance_top,
                          key.key_base.clearance_right,
                          key.key_base.clearance_bottom,
                          key.key_base.clearance_left,
                          key.cap.width,
                          key.cap.depth,
                          key.cap.thickness,
                          "tru" if key.key_base.is_visible else "fls"
                          ))

            col_idx = col_idx + 1
        last_row = row
        row_idx = row_idx + 1


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    construct_key_placement()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    if cliargs.export:
        a = cq.Assembly()
        for _pyo, cqo in objects:
            a = a.add(cqo)
        pc_3 = perf_counter()
        print("{:.3f}s elapsed for unifying objects".format(pc_3 - pc_2))

        filename = Path("{}/{}".format(cliargs.path, cliargs.filename)).name
        print("exporting to: {}".format(filename))
        cq.exporters.export(a, filename)
        pc_4 = perf_counter()
        print("{:.3f}s elapsed for export".format(pc_4 - pc_3))
else:
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    construct_key_placement()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))
    a = cq.Assembly()
    for pyo, cqo in objects:
        color = cq.Color(0, 0, 1, 0.5) if pyo.key_base.is_visible else cq.Color(1, 1, 1, 0.125)
        a.add(cqo, color=color)
    show_object(a)
