import importlib
from cli_args import cli_args


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def import_config():
    """
    prerequisites: any model is placed in src/keyboards/ and must provide
      - src/keyboards/<model_name>/config.py
        - class ModelConfig
    """
    args = cli_args()

    model_module = args.selected_model[0]

    importlib.invalidate_caches()
    model_config = importlib.import_module(".config", model_module)
    model_config.ModelConfig.matrix.layout_size = args.keyboard_size

    return args, model_config


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def import_builder():
    """
    prerequisites: any model is placed in src/keyboards/ and must provide
      - src/keyboards/<model_name>/builder.py
        - def compute(**kwargs) -> List[List[Key]]:
    """
    args = cli_args()
    model_module = args.selected_model[0]
    importlib.invalidate_caches()
    return importlib.import_module(".builder", model_module)
