from pathlib import Path
from time import perf_counter

from utils import *
from iso_keys import *
from iso_matrix import construct_key_placement, build_key_matrix
import cadquery as cq

pc_0 = perf_counter()
print("\nnstarted run {}".format(pc_0))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def compute() -> List[Tuple[Key, CadObjects]]:
    key_matrix = build_key_matrix()
    objects = construct_key_placement(key_matrix)
    return objects


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    objects = compute()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    if cliargs.export:
        assembly = cq.Assembly()
        for py_object, cad_objects in objects:
            if py_object.base.is_visible:
                for o in [value for _attr, value in cad_objects]:
                    assembly = assembly.add(o)

        pc_3 = perf_counter()
        print("{:.3f}s elapsed for unifying objects".format(pc_3 - pc_2))

        filename = Path("{}/{}".format(cliargs.path, cliargs.filename)).name
        print("exporting to: {}".format(filename))
        assembly.save(filename)
        pc_4 = perf_counter()
        print("{:.3f}s elapsed for export".format(pc_4 - pc_3))
    else:
        print("dry run: no export requested, just computed objects".format(pc_1 - pc_0))
else:
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    objects = compute()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    assembly = cq.Assembly()
    for py_object, cad_objects in objects:
        color = cq.Color(0, 0, 1, 0.5) if py_object.base.is_visible else cq.Color(1, 1, 1, 0.125)
        for o in [value for _attr, value in cad_objects]:
            assembly = assembly.add(o, color=color)

    show_object(assembly)

pc_1 = perf_counter()
print("{:.3f}s elapsed total".format(pc_1 - pc_0))
print("finished run {}\n".format(pc_0))
