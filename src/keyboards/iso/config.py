"""
All dimensions are metric in [mm].
"""
from typing import Optional


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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


class MatrixConfig(object):
    def __init__(self):
        # defined after command line arguments are parsed
        self.layout_size = None  # type: Optional["KeyboardSize"]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class ModelConfig(object):
    """
    Global configuration.
    """
    key_base = KeyBaseConfig()
    cap = KeyCapConfig()
    switch = KeySwitchConfig()
    switch_slot = KeySwitchSlotConfig()
    group = GroupConfig()
    matrix = MatrixConfig()
