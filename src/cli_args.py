import re
from typing import List, Tuple, Optional
import os.path
import argparse
from functools import wraps
from keyboard_size import KeyboardSize


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_eligible_models() -> List[Tuple[str, str, str]]:
    """
    Note: This method shall only be called from top level directory.
    @return: list of tuples of module name, model name and relative path
    """
    models_dir = "keyboards"
    abs_dir, file_name = os.path.split(os.path.abspath(__file__))
    abs_dir = os.path.join(abs_dir, models_dir)

    model_dirs = [d for d in os.listdir(abs_dir) if os.path.isdir(os.path.join(abs_dir, d))]
    model_dirs = [d for d in model_dirs if re.match(r"^[a-zA-Z]", d)]
    models: List[Tuple[str, str, str]] = list()

    for model_name in model_dirs:
        module_name = "src.keyboards.{}".format(model_name)
        models.append((module_name, model_name, "{}/{}".format(models_dir, model_name)))

    return models


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def parse_cli_once(cli_parser_f):
    @wraps(cli_parser_f)
    def wrapper():
        if wrapper.args is None:
            wrapper.args = cli_parser_f()
        return wrapper.args

    wrapper.args = None

    return wrapper


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@parse_cli_once
def cli_args() -> argparse.Namespace:
    default_size = KeyboardSize.S100
    eligible_models = get_eligible_models()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    layout_group = parser.add_argument_group("Layout")
    layout_group.add_argument("-m", "--matrix",
                              help="the keyboard style to compute",
                              default="iso",
                              choices=[m for _, m, _ in eligible_models])
    layout_group.add_argument("-k", "--keyboard-size",
                              help="the keyboard size to generate: influences the layout to compute, not the key size",
                              default=default_size.name,
                              choices=[e.name for e in KeyboardSize])
    layout_group.add_argument("-l", "--list",
                              help="list all discovered keyboard layouts and exit",
                              action="store_true")

    export_group = parser.add_argument_group("Export")
    export_group.add_argument("-e", "--export",
                              help="if specified export computed model to STEP file otherwise dry run; "
                                   "Exporting may take up to several minutes. For development load main.py "
                                   "with a cadquery editor (i.e. cq-editor).",
                              action="store_true")
    export_group.add_argument("-f", "--filename",
                              help="step file name",
                              default="split-planar-{}.step".format(default_size.name),
                              type=str)
    export_group.add_argument("-p", "--path",
                              help="path where to export",
                              default=os.getcwd(),
                              type=str)

    config_group = parser.add_argument_group("Configuration")
    config_group.description = "main config: cfg/debug.py, layout configs: /keyboards/<model_name>/config.py"

    parser.epilog = ("This script can be either started standalone or run by cadquery editor (cq-editor). "
                     "If run by cq-editor change the working directory to the src path, "
                     "start cq-editor and then load the file main.py. "
                     "Note: cq-editor's file watching feature cannot detect file changes of dynamically loaded modules "
                     "such as keyboard layouts.")

    args = parser.parse_args()

    if args.list is True:
        for package, layout, folder in eligible_models:
            print("{} in {}".format(layout, folder))
        exit(0)

    args.filename = "split-planar-{}.step".format(args.keyboard_size)
    args.keyboard_size = KeyboardSize.__dict__[args.keyboard_size]
    args.selected_model = [(m[0], m[1]) for m in eligible_models if m[1] == args.matrix][0]
    return args
