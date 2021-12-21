#!/usr/bin/env python3
from pathlib import Path
from time import perf_counter

from iso_keys import *
from iso_matrix import build_key_matrix, compute_placement_and_cad_objects, connect_horizontally
import cadquery

pc_0 = perf_counter()
print("\nnstarted run {}".format(pc_0))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def compute() -> List[Tuple[Key, CadObjects]]:
    key_matrix = build_key_matrix()
    objects = list()  # List[Tuple[Key, CadObjects]]
    compute_placement_and_cad_objects(key_matrix, objects)
    connect_horizontally(key_matrix, objects)

    #def loft_left_to_right(left: Key, right: Key):
    #    def get_wire(face):
    #        return face.first().wires().val()
    #
    #    left_wire = get_wire(left.slot.get_cad_face(Direction.RIGHT))
    #    right_wire = get_wire(right.slot.get_cad_face(Direction.LEFT))
    #    return cadquery.Solid.makeLoft([left_wire, right_wire])
    #
    #for row in key_matrix:
    #    print("xxx len(row) {}".format(len(row)))
    #    for ki in range(1, len(row)):
    #        left = row[ki - 1]
    #        right = row[ki]
    #        if left.base.is_connected and right.base.is_connected:
    #            print("xxx fuse l-r: {}-{}".format(left.name, right.name))
    #            x = CadObjects()
    #            x.slot = loft_left_to_right(left, right)
    #            objects.append((left, x))
    #    print("xxx ---")
    return objects


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    """
    command line invocation: compute, render and eventually export to step file
    """
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    objects = compute()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    if cliargs.export:
        assembly = cadquery.Assembly()
        union = None  # type: cadquery.Workplane
        for py_object, cad_objects in objects:
            if py_object.base.is_visible:
                for o in [value for _attr, value in cad_objects]:
                    if union is None:
                        union = o
                    else:
                        # TODO: clean=False required for freecad (fillet, chamfer, ...)
                        union = union.union(o, clean=False)
        assembly = assembly.add(union)

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
    """
    cadquery editor (cq-editor) section: compute, render and show_object()
    """
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - pc_0))
    objects = compute()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    assembly = cadquery.Assembly()
    union = None  # type: Optional[cadquery.Workplane]
    for py_object, cad_objects in objects:
        color = cadquery.Color(0, 0, 1, 0.5) if py_object.base.is_visible else cadquery.Color(1, 1, 1, 0.125)
        if not py_object.base.is_visible and not GlobalConfig.debug.show_invisibles:
            continue
        for o in [value for _attr, value in cad_objects]:
            if GlobalConfig.debug.render_unified:
                if union is None:
                    union = o
                else:
                    union = union.union(o)
            else:
                assembly = assembly.add(o, color=color)

    if GlobalConfig.debug.render_unified:
        assembly.add(union)
    show_object(assembly)

pc_1 = perf_counter()
print("{:.3f}s elapsed total".format(pc_1 - pc_0))
print("finished run {}\n".format(pc_0))
