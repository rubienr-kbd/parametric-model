#!/usr/bin/env python3
from pathlib import Path
from time import perf_counter

from iso_keys import *
from iso_matrix import build_key_matrix, compute_placement_and_cad_objects, get_key_connection_mapping, get_connector_connection_mapping
import cadquery

from utils import KeyUtils

pc_0 = perf_counter()
print("\nnstarted run {}".format(pc_0))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def compute() -> List[Tuple[Key, CadObjects]]:
    """
    strategy
      1. assemble key matrix: define key size and style(iso, ansi, with or without numpad/arrows etc.)
      2. optional: compute additional rotation/displacement if keyboard is not planar (not yet supported)
      3. compute real key placement and cad objects
      4. connect keys (split keyboard: not yet supported)
      5. construct wall around keys (not yet supported)
      6. construct bottom plate (not yet supported)
    """

    # 1.
    key_matrix = build_key_matrix()
    # 2. not implemented
    # 3.
    computed_objects = compute_placement_and_cad_objects(key_matrix)
    # 4.
    conn_map = get_key_connection_mapping(key_matrix)
    connections = KeyUtils.connect_keys(conn_map, key_matrix)
    conn_map = get_connector_connection_mapping(key_matrix)
    connections.extend(KeyUtils.connect_connectors(conn_map, key_matrix))

    for k, _, c in connections:
        x = CadObjects()
        x.cap = c
        computed_objects.append((k, x))

    # 5. not implemented
    # 6. not implemented
    return computed_objects


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
        union = None  # type: Optional[cadquery.Workplane]
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
