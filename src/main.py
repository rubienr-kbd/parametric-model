#!/usr/bin/env python3
import os
import sys
import re

# cq-editor workaround: if main.py is loaded by cq-editor then sys.path is not set as expected and the modules to load won't be found.
# In order to work, cq-editor must be started from the src folder.
paths = [os.getcwd(), re.sub(".src$", "", os.getcwd())]
[sys.path.insert(0, p) for p in paths if p not in sys.path]

from pathlib import Path
from time import perf_counter
from model_importer import import_config, import_builder
from cfg.debug import DEBUG
import cadquery
from keys.utils import KeyUtils

cliargs, model_config = import_config()
builder = import_builder()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def run(perf_counter_begin: float) -> None:
    pc_1 = perf_counter()
    is_invoked_by_cli = __name__ == "__main__"
    do_unify = DEBUG.export_unified if is_invoked_by_cli else DEBUG.render_unified
    do_clean_union = DEBUG.export_cleaned_union if is_invoked_by_cli else DEBUG.render_cleaned_union

    print("{:.3f}s elapsed for loading".format(pc_1 - perf_counter_begin))
    key_matrix = builder.compute(do_unify=do_unify)
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
