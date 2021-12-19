from pathlib import Path
from time import perf_counter

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
        print("  col|x       y     z   |key   unit|clrto clrri clrbo clrle|capwi  capde capth|vis")
        print("  --------------------------------------------------------------------------------")
        is_first_key_in_row = True
        col_idx = 0

        for key in row:
            key.update()
            if is_first_key_in_row:
                if last_row is not None:
                    KeyUtils.set_position_relative_to(key.base, last_row[0].base, Direction.TOP)
                key.base.align_to_position(0, Direction.LEFT)
            elif last_key is not None:
                KeyUtils.set_position_relative_to(key.base, last_key.base, Direction.RIGHT)
            is_first_key_in_row = False
            last_key = key

            key.compute()

            if key.cad_objects.plane:
                objects.append((key, key.cad_objects.plane))
            if key.cad_objects.name:
                objects.append((key, key.cad_objects.name))
            if key.cad_objects.cap and key.base.is_visible:
                objects.append((key, key.cad_objects.cap))
            if key.cad_objects.origin:
                objects.append((key, key.cad_objects.origin))
            if key.cad_objects.slot:
                objects.append((key, key.cad_objects.slot))

            print("  {col:2} |{x:6.2f}{y:6.2f}{z:6.2f}|{key:5} {unit:4.2f}|{clrto:5.2f} {clrri:5.2f} {clrbo:5.2f} {clrle:5.2f}|{capwi:6.2f} {capde:5.2f} {capth:5.2f}|{vis}"
                  .format(col=col_idx,
                          x=key.base.position[0], y=key.base.position[1], z=key.base.position[2],
                          key=key.name,
                          unit=key.base.unit_width_factor,
                          clrto=key.base.clearance_top,
                          clrri=key.base.clearance_right,
                          clrbo=key.base.clearance_bottom,
                          clrle=key.base.clearance_left,
                          capwi=key.cap.width,
                          capde=key.cap.depth,
                          capth=key.cap.thickness,
                          vis="yes" if key.base.is_visible else "no "))

            col_idx = col_idx + 1
        last_row = row
        row_idx = row_idx + 1


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print("\n\n\n")

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
        color = cq.Color(0, 0, 1, 0.5) if pyo.base.is_visible else cq.Color(1, 1, 1, 0.125)
        a.add(cqo, color=color)
    show_object(a)

pc_1 = perf_counter()
print("{:.3f}s elapsed total".format(pc_1 - pc_0))
