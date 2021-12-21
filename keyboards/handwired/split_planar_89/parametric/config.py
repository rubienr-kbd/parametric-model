import os
from enum import Enum
import argparse

"""
All dimensions are metric in [mm].
"""


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyboardSize(Enum):
    """
    KeyboardSize.S100 : 100% ... inclusive: f-row, number-row, arrow keys, pg-up/down group and numpad
    KeyboardSize.S80  :  80% ... inclusive: f-row, number-row, arrow keys, pg-up/down group
    KeyboardSize.S75  :  75% ... inclusive: f-row, number-row, ins/del, home/end, pg-up/down
    KeyboardSize.S65  :  69% ... inclusive: number-row, del, home, pg-up/down
    KeyboardSize.S60  :  60% ... inclusive: number-row
    KeyboardSize.S40  :  40% ... mainly characters
    """
    S100 = 100
    S80 = 80
    S75 = 75
    S65 = 65
    S60 = 60
    S40 = 40


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class DebugConfig(object):
    def __init__(self):
        """
        Parameters
        ----------
        self.debug_enable: global switch for debug/release
        self.show_placement: renders a wire outlining the key placement upon all subsequent key objects are placed relative to
        self.show_key_name: renders the key name in the placement face
        self.show_key_cap: renders the key cap
        self.show_key_origin: emphasize each key origin (x/y-center) by small circle
        self.show_invisibles: renders placeholder components
        self.disable_object_cache: deactivate cad object caching, otherwise re-use pre-computed objects (performance factor about 5)
        self.render_unify_in_cadquery_editor: unifies the rendered view in cq-editor (does not affect export to file)
        """
        self.debug_enable = True  # type: bool
        self.show_placement = False  # type: bool
        self.show_key_origin = False  # type: bool
        self.show_key_name = False  # type: bool
        self.show_key_cap = False  # type: bool
        self.show_key_switch = False  # type: bool
        self.show_invisibles = False  # type: bool
        self.disable_object_cache = False  # type: bool
        self.unify_in_cadquery_editor = False  # type: bool

    @property
    def render_key_placement(self):
        return self.debug_enable and self.show_placement

    @property
    def render_origin(self):
        return self.debug_enable and self.show_key_origin

    @property
    def render_key_name(self):
        return self.debug_enable and self.show_placement and self.show_key_name

    @property
    def render_key_cap(self):
        return self.debug_enable and self.show_key_cap

    @property
    def render_invisibles(self):
        return self.debug_enable and self.show_invisibles

    @property
    def render_key_switch(self):
        return self.debug_enable and self.show_key_switch

    @property
    def render_unified(self):
        return self.unify_in_cadquery_editor


class KeyBaseConfig(object):
    def __init__(self):
        """
        self.unit_length : the center to center distance of two adjacent keys in the same row; usually 19mm
        self.clearance_x : extra clearance for the vertical gap width  in between two adjacent keys in the same row; usually 0mm
        self.clearance_y : extra clearance for the horizontal gap width in between two neighbouring rows: usually 0mm
        """
        self.unit_length = 19  # type: float
        self.clearance_x = 0 / 2  # type: float
        self.clearance_y = 0 / 2  # type: float


class KeyCapConfig(object):
    """

    Attribures:
        self.width_clearance: width of the vertical gap in between two neighbouring keys in the same row
        self.depth_clearance : width of the horizontal gap in between two neighbouring rows
        self.thickness : height to 3-d sketch the key cap
        self.z_clearance : distance in between base plane and the bottom of the key cap
        self.dish_inset : the tapering on the top (dish) for each side
    """

    def __init__(self):
        """
        Aim: parameters are used to roughly illustrate the key cap placement
        Non aim: render the key shape in detail or even SA/OEM/etc. shape

        self.width_clearance : width of the vertical gap in between two neighbouring keys in the same row
        self.depth_clearance : width of the horizontal gap in between two neighbouring rows
        self.thickness : height to 3-d sketch the key cap
        self.z_clearance : distance in between base plane and the bottom of the key cap
        self.dish_inset : the tapering on the top (dish) for each side
        """
        # ensure that: clearance + width + clearance == unit_length
        self.width_clearance = 2  # type: float
        self.depth_clearance = 2  # type: float
        self.thickness = 9  # type: float
        self.z_clearance = 6  # type: float
        self.dish_inset = 1  # type: float


class KeySwitchConfig(object):

    def __init__(self):
        """
        Arguments do sketch the necessary details of a single switch.
        """
        self.width = 18  # type: float
        self.depth = 18  # type: float
        self.thickness = 4  # type: float


class KeySwitchSlotConfig(object):

    def __init__(self):
        """
        Arguments to sketch the necessary cutout for a single switch.

        self.width : slot width (length in x direction)
        self.depth : slot depth (length in y direction)
        self.thickness : total thickness of top skin wall (length in z direction)
        self.undercut_width : length of undercut
        self.undercut_undercut_depth : horizontal inset of undercut below top skin
        self.undercut_thickness : thickness of top skin face to top/beginning of undercut (length in z direction)
        """
        self.width = 14  # type: float
        self.depth = 14  # type: float
        self.thickness = 4  # type: float
        self.undercut_width = 6  # type: float
        self.undercut_depth = 1  # type: float
        self.undercut_thickness = 1.25  # type: float


class GroupConfig(object):

    def __init__(self):
        """
        Additional extra clearance for
          - F1, F5, F9 and Print
          - print, insert, delete and left arrow
          - left column of numpad keys

        self.clearance_x_f_group : horizontal clearance in between ESC-F1, F4-F5 and F8-F9; should be unit_length * num_lesser_keys / num_gaps
        self.clearance_y_f_group : vertical clearance in between F row and number row
        self.clearance_x_arrow_group : horizontal clearance in between LAR-RCTL, ENT-INS, BSP-INS and F12-PRT
        self.clearance_x_numpad : horizontal clearance in between arrow-group and numpad (RAR-0, PDN-7, PUP-NUM)
        """
        self.clearance_x_f_group = 19 * 2 / 3  # type: float
        self.clearance_y_f_group = 4  # type: float
        self.clearance_x_arrow_group = 10  # type: float
        self.clearance_x_numpad = 10  # type: float


class ArrowGroupConfig(object):

    def __init__(self):
        """
        Additional extra arguments for arrow keys group.
        """
        self.clearance_x = 14  # type: float


class MatrixConfig(object):
    def __init__(self):
        self.layout_size = KeyboardSize.S100  # type: KeyboardSize


class GlobalConfig(object):
    """
    Global configuration.
    """
    debug = DebugConfig()
    key_base = KeyBaseConfig()
    cap = KeyCapConfig()
    switch = KeySwitchConfig()
    switch_slot = KeySwitchSlotConfig()
    group = GroupConfig()
    arrow_group = ArrowGroupConfig()
    matrix = MatrixConfig()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-k", "--keyboard-size", help="keyboard size to generate; influences the layout to compute, not the key size", default=GlobalConfig.matrix.layout_size.name,
                        choices=[e.name for e in KeyboardSize])
    parser.add_argument("-e", "--export", help="export to STEP file (see --filename, --path)", action="store_true")
    parser.add_argument("-f", "--filename", help=".step file name", default="split-planar-{}.step".format(GlobalConfig.matrix.layout_size.name), type=str)
    parser.add_argument("-p", "--path", help="path where to export", default=os.getcwd(), type=str)

    args = parser.parse_args()
    GlobalConfig.matrix.layout_size = KeyboardSize.__dict__[args.keyboard_size]
    args.filename = "split-planar-{}.step".format(args.keyboard_size)
    return args


cliargs = parse_cli_args()
