from enum import Enum
import argparse


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyboardSize(Enum):
    """
    S100 = 100% ... inclusive: f-row, number-row, arrow keys, pg-up/down group and numpad
    S80  =  80% ... inclusive: f-row, number-row, arrow keys, pg-up/down group
    S75  =  75% ... inclusive: f-row, number-row, ins/del, home/end, pg-up/down
    S65  =  69% ... inclusive: number-row, del, home, pg-up/down
    S60  =  60% ... inclusive: number-row
    S40  =  40% ... mainly characters
    """
    S100 = 1
    S80 = 2
    S75 = 3
    S65 = 4
    S60 = 5
    S40 = 6


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# all dimensions are metric in mm


class KeyBaseConfig(object):
    def __init__(self):
        # center to center distance of two 1-uni keys
        self.unit_length = 19.0  # type: float
        # half of clearance in-between two keys
        self.clearance_x = 1 / 2.0  # type: float
        self.clearance_y = 1 / 2.0  # type: float


class KeyCapConfig(object):
    """
    Key cap related parameter.
    Aim: roughly illustrate the key cap placement
    Non aim: fully render key shape nor the height depending on row
    """

    def __init__(self):
        # ensure that: width + clearance + clearance == unit_length
        self.width = 18.0  # type: float
        self.depth = 18.0  # type: float
        self.thickness = 9.0  # type: float


class KeySwitchConfig(object):
    """
    Arguments do sketch the necessary details of a single switch.
    """

    def __init__(self):
        self.width = 18.0  # type: float
        self.depth = 18.0  # type: float
        self.thickness = 4.0  # type: float


class KeySwitchSlotConfig(object):
    """
    Arguments to sketch the necessary cutout for a single switch.
    """

    def __init__(self):
        self.width = 18.0  # type: float
        self.depth = 18.0  # type: float
        self.thickness = 4.0  # type: float
        self.clearance_x = 1.0  # type: float
        self.clearance_y = 1.0  # type: float
        self.clearance_f_group_x = 14.0  # type: float
        self.clearance_arrow_group_x = 14.0  # type: float


class GroupConfig(object):
    """
    Additional extra clearance for
      - F1, F5, F9 and Print
      - print, insert, delete and arrows
      - numpad
    """

    def __init__(self):
        self.clearance_x_f_group = 14.0  # type: float
        self.clearance_x_arrow_group = 14.0  # type: float
        self.clearance_x_numpad = 14.0  # type: float


class ArrowGroupConfig(object):
    """
    Additional extra arguments for arrow keys group.
    """

    def __init__(self):
        self.clearance_x = 14.0  # type: float


class MatrixConfig(object):
    def __init__(self):
        layout_size = KeyboardSize.S100  # type: KeyboardSize


class GlobalConfig(object):
    """
    Global configuration.
    """
    key_base = KeyBaseConfig()
    cap = KeyCapConfig()
    switch = KeySwitchConfig()
    switch_slot = KeySwitchSlotConfig()
    group = GroupConfig()
    arrow_group = ArrowGroupConfig()
    matrix = MatrixConfig()


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-k", "--keyboard-size", help="keyboard size to generate; influences the layout to compute, not the key size", default=KeyboardSize.S80.name,
                        choices=[e.name for e in KeyboardSize])
    parser.add_argument("-e", "--export", help="export to STEP file (see --filename, --path)", action="store_true")
    parser.add_argument("-f", "--filename", help=".step file name", default="split-planar-{}.step".format(KeyboardSize.S80.name), type=str)
    parser.add_argument("-p", "--path", help="path where to export", default="./", type=str)

    args = parser.parse_args()
    GlobalConfig.matrix.layout_size = KeyboardSize.__dict__[args.keyboard_size]
    args.filename = "split-planar-{}.step".format(args.keyboard_size)
    return args


cliargs = parse_cli_args()
