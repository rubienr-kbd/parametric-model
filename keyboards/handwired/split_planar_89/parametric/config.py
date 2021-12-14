

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# all dimensions are metric in mm

class KeyBaseConfig(object):
    def __init__(self):
        # center to center distance of two 1-uni keys
        self.unit_length = 19  # type: float
        # half of clearance in-between two keys
        self.clearance_x = 1/2  # type: float
        self.clearance_y = 1/2  # type: float


class KeyCapConfig(object):
    """
    Key cap related parameter.
    Aim: roughly illustrate the key cap placement
    Non aim: fully render key shape nor the height depending on row
    """
    def __init__(self):
        # ensure that: width + clearance + clearance == unit_length
        self.width = 18  # type: float
        self.depth = 18  # type: float
        self.thickness = 9  # type: float


class KeySwitchConfig(object):
    """
    Arguments do sketch the necessary details of a single switch.
    """
    def __init__(self):
        self.width = 18  # type: float
        self.depth = 18  # type: float
        self.thickness = 4  # type: float


class KeySwitchSlotConfig(object):
    """
    Arguments to sketch the necessary cutout for a single switch.
    """
    def __init__(self):
        self.width = 18  # type: float
        self.depth = 18  # type: float
        self.thickness = 4  # type: float
        self.clearance_x = 1  # type: float
        self.clearance_y = 1  # type: float
        self.clearance_f_group_x = 14  # type: float
        self.clearance_arrow_group_x = 14  # type: float


class FGroupConfig(object):
    """
    Additional extra arguments for F-1 to F-12 groups.
    """
    def __init__(self):
        self.clearance_x = 14  # type: float


class ArrowGroupConfig(object):
    """
    Additional extra arguments for arrow keys group.
    """
    def __init__(self):
        self.clearance_x = 14  # type: float


class GlobalConfig(object):
    """
    Global configuration.
    """
    key_base = KeyBaseConfig()
    cap = KeyCapConfig()
    switch = KeySwitchConfig()
    switch_slot = KeySwitchSlotConfig()
    f_group = FGroupConfig()
    arrow_group = ArrowGroupConfig()
