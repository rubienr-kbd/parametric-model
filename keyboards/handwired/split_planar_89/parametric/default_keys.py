from key import *

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Key100Unit(Key):
    def __init__(self) -> None:
        super(Key100Unit, self).__init__()
        self.name = "u100"


class Key100UnitSpacer(Key):
    def __init__(self) -> None:
        super(Key100UnitSpacer, self).__init__()
        self.name = "su100"
        self.base.is_visible = False


class Key125UnitSpacer(Key):
    def __init__(self) -> None:
        super(Key125UnitSpacer, self).__init__()
        self.name = "su125"
        self.base.unit_width_factor = 1.25
        self.base.is_visible = False


class Key125Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key125Unit, self).__init__()
        self.name = "u125"
        self.base.unit_width_factor = 1.25


class Key150Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key150Unit, self).__init__()
        self.name = "u150"
        self.base.unit_width_factor = 1.5


class Key175Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key175Unit, self).__init__()
        self.name = "u175"
        self.base.unit_width_factor = 1.75


class Key200Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key200Unit, self).__init__()
        self.name = "u200"
        self.base.unit_width_factor = 2


class Key225Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key225Unit, self).__init__()
        self.name = "u225"
        self.base.unit_width_factor = 2.25


class Key250Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key250Unit, self).__init__()
        self.name = "u250"
        self.base.unit_width_factor = 2.5


class Key275Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key275Unit, self).__init__()
        self.name = "u275"
        self.base.unit_width_factor = 2.75


class Key300Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key300Unit, self).__init__()
        self.name = "u300"
        self.base.unit_width_factor = 3


class Key400Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key400Unit, self).__init__()
        self.name = "u400"
        self.base.unit_width_factor = 4


class Key500Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key500Unit, self).__init__()
        self.name = "u500"
        self.base.unit_width_factor = 5


class Key600Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key600Unit, self).__init__()
        self.name = "u600"
        self.base.unit_width_factor = 6


class Key625Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key625Unit, self).__init__()
        self.name = "u625"
        self.base.unit_width_factor = 6.25


class Key700Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key700Unit, self).__init__()
        self.name = "u700"
        self.base.unit_width_factor = 7

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
