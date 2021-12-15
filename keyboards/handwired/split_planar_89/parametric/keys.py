from typing import List, Optional
from cadquery import Shape
from config import *

"""
Indexing and terms:

             first key (keys are not aligned to columns)
             ↓
         ╭───────────────────────────────────────────────────────────────────────────────────────╮
row 5 →  │  ESC F1  F2  F3  F4  F5  F6  F7  F8  F9 F10 F11 F12   PR  SL  PA                      │
         │  ^    1   2   3   4   5   6   7   8   9   0  ... BS   INS P1  PUP   NUM  /  *     -   │
         │  TAB  q w e r ...                              ISOE   DEL END PDN    7   8   9    +   │
         │  CLK  a s d f ...                               ISO                  4   5   6    +   │
         │  LSF  < y x c ...                               RSF        ↑         1   2   3  ENTER │
row 0 →  │  LCTL ... LALT           SPACE        RALT ... RCTL    ←   ↓   →    INS INS DEL ENTER │
         ╰───────────────────────────────────────────────────────────────────────────────────────╯

- row left/right direction may be aso denoted as x, x-direciton or x-axis
- row up/down direction may also be denoted as y, y-direction or y-axis

- key/switch
  - width            ... x-axis
  - depth            ... y-axis
  - height/thickness ... z-axis

Key cap vs. switch/stabilizer position:
The key origin, as seen from z+ axis, is to the center of width (except iso-enter, numpad-enter, numpad+) in x direction,
and the center of top row.
The switches share mostly (but not mandatorily) the same center in x/y plane.

⊙ ... origin
⊛ ... origin + switch
⨂ ... origin + stabilizer
* ... switch
⨯ ... stabilizer

         ↓ 2 unit key                      iso enter ↓      ↓ numpad enter or +
╭───╮╭───────╮╭─────────────────────────────────╮ ╭─────╮ ╭───╮
│ ⊛ ││   ⊛   ││   ⨯           ⊛            ⨯    │ │  ⨂  │ │ ⨂ │
╰───╯╰───────╯╰─────────────────────────────────╯ ╰╮ *  │ │ * │
  ↑ 1 unit key                ↑ space              │ ⨯  │ │ ⨯ │
                                                   ╰────╯ ╰───╯
"""


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyBase(object):
    def __init__(self, config: KeyBaseConfig) -> None:
        self.unit_length = config.unit_length  # type: float
        self.unit_factor = 1  # type: float
        self.clearance_left = config.clearance_x
        self.clearance_right = config.clearance_x
        self.clearance_top = config.clearance_y
        self.clearance_bottom = config.clearance_y
        self.position = [0, 0, 0]  # type: List[float, float, float]
        self.rotation = [0, 0, 0]  # type: List[float, float, float]

    def set_position_relative_to(self, ref_key, pos: Direction) -> None:
        if pos == Direction.TOP:
            self.position[0] = ref_key.position[0]
            self.position[1] = ref_key.position[1] + ref_key.unit_length / 2 + ref_key.clearance_top + self.clearance_bottom + self.unit_length / 2

        elif pos == Direction.RIGHT:
            self.position[0] = ref_key.position[0] + ref_key.unit_length / 2 + ref_key.clearance_right + self.clearance_left + self.unit_length / 2
            self.position[1] = ref_key.position[1]

        elif pos == Direction.BOTTOM:
            self.position[0] = ref_key.position[0]
            self.position[1] = ref_key.position[1] - ref_key.unit_length / 2 - ref_key.clearance_bottom - self.clearance_top - self.unit_length / 2

        elif pos == Direction.LEFT:
            self.position[0] = ref_key.position[0] - ref_key.unit_length / 2 - ref_key.clearance_left - self.clearance_right - self.unit_length / 2
            self.position[1] = ref_key.position[1]

    def set_key_unit_factor(self, unit_factor: float):
        self.unit_factor = unit_factor
        self.unit_length = GlobalConfig.key_base.unit_length * self.unit_factor


class KeyCap(object):
    def __init__(self, config: KeyCapConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class KeySwitch(object):
    def __init__(self, config: KeySwitchConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class KeySwitchSlot(object):
    def __init__(self, config: KeySwitchSlotConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class CadqueryObject(object):
    def __init__(self):
        self.key = None  # type: Optional[Shape]
        self.switch = None  # type: Optional[Shape]
        self.slot = None  # type: Optional[Shape]


class Key(object):
    def __init__(self) -> None:
        self.key_base = KeyBase(GlobalConfig.key_base)
        self.cap = KeyCap(GlobalConfig.cap)
        self.switch = KeySwitch(GlobalConfig.switch)
        self.switch_slot = KeySwitch(GlobalConfig.switch_slot)
        self.cq = CadqueryObject()
        self.key_base.set_key_unit_factor(1)

        self.name = ""


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Key100Unit(Key):
    def __init__(self) -> None:
        super(Key100Unit, self).__init__()
        self.name = "u100"


class Key100UnitSpacer(Key):
    def __init__(self) -> None:
        super(Key100UnitSpacer, self).__init__()
        self.name = "us100"


class Key100UnitNumpadSpacer(Key):
    """
    for spacing the numpad
    """

    def __init__(self) -> None:
        super(Key100UnitNumpadSpacer, self).__init__()
        self.name = "uns100"
        self.clearance_left = GlobalConfig.group.clearance_x_f_group


class Key100UnitUpArrowSpacer(Key):
    """
    for spacing the arrow-up key
    """

    def __init__(self) -> None:
        super(Key100UnitUpArrowSpacer, self).__init__()
        self.name = "uas100"
        self.clearance_left = GlobalConfig.group.clearance_x_f_group


class Key111Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key111Unit, self).__init__()
        self.name = "u1.111"
        self.key_base.set_key_unit_factor(1.1111)


class Key125Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key125Unit, self).__init__()
        self.name = "125"
        self.key_base.set_key_unit_factor(1.25)


class Key150Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key150Unit, self).__init__()
        self.name = "150"
        self.key_base.set_key_unit_factor(1.5)


class Key175Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key175Unit, self).__init__()
        self.name = "175"
        self.key_base.set_key_unit_factor(1.75)


class Key200Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key200Unit, self).__init__()
        self.name = "200"
        self.key_base.set_key_unit_factor(2)


class Key225Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key225Unit, self).__init__()
        self.name = "225"
        self.key_base.set_key_unit_factor(2.25)


class Key250Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key250Unit, self).__init__()
        self.name = "250"
        self.key_base.set_key_unit_factor(2.5)


class Key275Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key275Unit, self).__init__()
        self.name = "275"
        self.key_base.set_key_unit_factor(2.75)


class Key300Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key300Unit, self).__init__()
        self.name = "300"
        self.key_base.set_key_unit_factor(3)


class Key400Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key400Unit, self).__init__()
        self.name = "400"
        self.key_base.set_key_unit_factor(4)


class Key500Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key500Unit, self).__init__()
        self.name = "500"
        self.key_base.set_key_unit_factor(5)


class Key566Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key566Unit, self).__init__()
        self.name = "566"
        self.key_base.set_key_unit_factor(5.6667)


class Key600Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key600Unit, self).__init__()
        self.name = "600"
        self.key_base.set_key_unit_factor(6)


class Key700Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key700Unit, self).__init__()
        self.name = "700"
        self.key_base.set_key_unit_factor(7)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyUtils(object):

    #    @staticmethod
    #    def update_next_key_pos_in_row(key: Key, next_key: Key) -> None:
    #
    #        p = KeyUtils.compute_next_key_pos_in_row(key, next_key)
    #        p.p_position[1] = key.p_position[1]
    #        p.p_position[2] = key.p_position[2]
    #        next_key.p_position.clear()
    #        next_key.p_position.extend(p.p_position)

    @staticmethod
    def update_key_pos_in_row(row: List[Key]) -> None:
        """
        :param row: list of keys (row) to update in y direction according to the first key
        """
        for (i_left, i_right) in [ilr for ilr in zip(range(len(row) - 1), range(1, len(row)))]:
            key_left = row[i_left]
            key_right = row[i_right]
            key_right.key_base.set_position_relative_to(key_left.key_base, Direction.RIGHT)

    #    @staticmethod
    #   def compute_next_row_pos(key: Optional[Key], next_key: Key) -> Placement:
    #        p = Placement()
    #        p.p_rotation = key.p_rotation
    #        p.p_position = key.p_position
    #        p.p_position[1] = key.p_position[1] + key.b_depth / 2 + KeyConfig.switch.clearance_y + next_key.b_depth / 2
    #        return p
    #
    #    @staticmethod
    #    def update_next_row_pos(key: Optional[Key], next_row_key: Key) -> None:
    #        p = KeyUtils.compute_next_row_pos(key, next_row_key)
    #        p.p_position[0] = next_row_key.p_position[0]
    #        p.p_position[2] = next_row_key.p_position[2]
    #        next_row_key.p_position.clear()
    #        next_row_key.p_position.extend(p.p_position)
    #

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
