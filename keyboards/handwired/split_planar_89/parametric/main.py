#!/usr/bin/env python3
import importlib
from pathlib import Path
from time import perf_counter

from iso_keys import *
from utils import KeyUtils

kbd_matrix_builder = importlib.import_module(cliargs.matrix)
import cadquery


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def run(perf_counter_begin: float) -> None:
    pc_1 = perf_counter()
    print("{:.3f}s elapsed for loading".format(pc_1 - perf_counter_begin))
    key_matrix = kbd_matrix_builder.compute()
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    do_unify = cliargs.export
    # TODO: do_clean_union=False required for freecad (otherwise experienced issues with fillet, chamfer)
    do_clean_union = False

    squashed = KeyUtils.squash(key_matrix, do_unify=do_unify, do_clean_union=do_clean_union)
    pc_3 = perf_counter()
    print("{:.3f}s elapsed for unifying objects".format(pc_3 - pc_2))

    if cliargs.export:
        filename = Path("{}/{}".format(cliargs.path, cliargs.filename)).name
        print("exporting to: {}".format(filename))
        cadquery.Assembly().add(squashed).save(filename)
        pc_4 = perf_counter()
        print("{:.3f}s elapsed for export".format(pc_4 - pc_3))
    else:
        show_object(squashed)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


pc_0 = perf_counter()
print("\nstarted run at {:.3f}".format(pc_0))
run(perf_counter_begin=pc_0)
pc_1 = perf_counter()
print("{:.3f}s elapsed total".format(pc_1 - pc_0))
print("finished run at {:.3f}\n".format(pc_0))
