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
    is_invoked_by_cli = __name__ == "__main__"
    do_unify = GlobalConfig.debug.export_unified if is_invoked_by_cli else GlobalConfig.debug.render_unified
    do_clean_union = GlobalConfig.debug.export_cleaned_union if is_invoked_by_cli else GlobalConfig.debug.render_cleaned_union

    print("{:.3f}s elapsed for loading".format(pc_1 - perf_counter_begin))
    key_matrix = kbd_matrix_builder.compute(for_export=cliargs.export)
    pc_2 = perf_counter()
    print("{:.3f}s elapsed for construction".format(pc_2 - pc_1))

    squashed = KeyUtils.squash(key_matrix, do_unify=do_unify, do_clean_union=do_clean_union)
    pc_3 = perf_counter()
    print("{:.3f}s elapsed for unifying objects".format(pc_3 - pc_2))

    if is_invoked_by_cli:
        if cliargs.export:
            filename = os.path.abspath(os.path.join(cliargs.path, cliargs.filename))
            print("exporting to: {}".format(filename))
            cadquery.Assembly().add(squashed).save(filename)
            print("exported to: {} size: {:,} kB".format(filename, Path(filename).stat().st_size))
            pc_4 = perf_counter()
            print("{:.3f}s elapsed for export".format(pc_4 - pc_3))
    else:
        show_object(squashed)

    print("\ninvocation:")
    print("  invoked by:                        {}".format("command line" if is_invoked_by_cli else "cadquery editor"))
    if is_invoked_by_cli:
        print("  export requested:                  {}".format("yes" if cliargs.export else "no (dry run)"))
    print("  unify vs. assembly:                {}".format("unify" if do_unify else "assembly"))
    if do_unify:
        print("  clean to have a clean shape union: {}".format("yes" if do_clean_union else "no"))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


pc_0 = perf_counter()
print("\nstarted run at {:.3f}".format(pc_0))
run(perf_counter_begin=pc_0)
pc_5 = perf_counter()
print("\n{:.3f}s elapsed total".format(pc_5 - pc_0))
print("finished run at {:.3f}\n".format(pc_0))
