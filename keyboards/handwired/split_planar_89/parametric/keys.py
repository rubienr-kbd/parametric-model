from typing import List, Optional
from cadquery import Shape
from config import *
from cq_mixins import *

"""
Indexing and terms:

             first key (keys are not aligned to columns)
             ↓
         ╭─────────────────────────────────────────────────────────────────────────────────────╮
row 5 →  │  ESC F1  F2  F3  F4  F5  F6  F7  F8  F9 F10 F11 F12  PR  SL  PA        .   .   .    │
         │   ^   1   2   3   4   5   6   7   8   9   0  ... ←   INS P1  PUP    NUM  /   *   -  │
         │   ⇄   q w e r ...                                ↲   DEL END PDN     7   8   9   +  │
         │   ⇓   a s d f ...                                ↲                   4   5   6   +  │
         │   ⇑   < y x c ...                                ⇑         ↑         1   2   3  ENT │
row 0 →  │  LCTL ... LALT           SPACE        RALT ... RCTL    ←   ↓   →    INS INS DEL ENT │
         ╰─────────────────────────────────────────────────────────────────────────────────────╯

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
    FRONT = 5
    BACK = 6


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyBase(CqBoxMixin):
    def __init__(self, config: KeyBaseConfig) -> None:
        self.unit_length = config.unit_length  # type: float
        self.unit_width_factor = 1.0  # type: float
        self.unit_depth_factor = 1.0  # type: float
        self.clearance_left = config.clearance_x
        self.clearance_right = config.clearance_x
        self.clearance_top = config.clearance_y
        self.clearance_bottom = config.clearance_y
        self.position = [0, 0, 0]  # type: List[float, float, float]
        self.rotation = [0, 0, 0]  # type: List[float, float, float]
        self.is_visible = True

    @property
    def width(self) -> float:
        return self.unit_width_factor * self.unit_length

    @property
    def depth(self) -> float:
        return self.unit_depth_factor * self.unit_length

    @property
    def thickness(self):
        return 0.1

    def set_position_relative_to(self, ref_key, pos: Direction) -> None:
        """
        Defines our position as top/bottom left/right of the reference key.
        """
        if pos == Direction.TOP:
            self.position[1] = ref_key.position[1] + ref_key.depth / 2 + ref_key.clearance_top + self.clearance_bottom + self.depth / 2
            self.position[0] = ref_key.position[0]
        elif pos == Direction.BOTTOM:
            self.position[1] = ref_key.position[1] - ref_key.depth / 2 - ref_key.clearance_bottom - self.clearance_top - self.depth / 2
            self.position[0] = ref_key.position[0]

        elif pos == Direction.RIGHT:
            self.position[0] = ref_key.position[0] + ref_key.width / 2 + ref_key.clearance_right + self.clearance_left + self.width / 2
            self.position[1] = ref_key.position[1]
        elif pos == Direction.LEFT:
            self.position[0] = ref_key.position[0] - ref_key.width / 2 - ref_key.clearance_left - self.clearance_right - self.width / 2
            self.position[1] = ref_key.position[1]

        else:
            assert False

    def align_to_position(self, position: float, pos: Direction) -> None:
        """
        Aligns our bounding box top/bottom left/right front/top to position (x, y or z-axis).
        """
        if pos == Direction.TOP:
            self.position[2] = position - self.thickness / 2
        elif pos == Direction.BOTTOM:
            self.position[2] = position + self.thickness / 2
        elif pos == Direction.RIGHT:
            self.position[0] = position - self.width / 2
        elif pos == Direction.LEFT:
            self.position[0] = position + self.width / 2
        elif pos == Direction.FRONT:
            self.position[1] = position + self.depth / 2
        elif pos == Direction.BACK:
            self.position[1] = position - self.depth / 2



class KeyCap(CqBoxMixin):
    def __init__(self, config: KeyCapConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class KeySwitch(CqBoxMixin):
    def __init__(self, config: KeySwitchConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class KeySwitchSlot(CqBoxMixin):
    def __init__(self, config: KeySwitchSlotConfig) -> None:
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class CadqueryObject(object):
    def __init__(self):
        self.key = None  # type: Optional[Shape]
        self.switch = None  # type: Optional[Shape]
        self.slot = None  # type: Optional[Shape]


class Key(KeyMixin, CqKeyMixin):
    def __init__(self) -> None:
        self.key_base = KeyBase(GlobalConfig.key_base)
        self.cap = KeyCap(GlobalConfig.cap)
        self.switch = KeySwitch(GlobalConfig.switch)
        self.switch_slot = KeySwitch(GlobalConfig.switch_slot)
        self.cq = CadqueryObject()

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
        self.key_base.is_visible = False


class Key125Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key125Unit, self).__init__()
        self.name = "u125"
        self.set_key_width_unit_factor(1.25)


class Key150Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key150Unit, self).__init__()
        self.name = "u150"
        self.set_key_width_unit_factor(1.5)


class Key175Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key175Unit, self).__init__()
        self.name = "u175"
        self.set_key_width_unit_factor(1.75)


class Key200Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key200Unit, self).__init__()
        self.name = "u200"
        self.set_key_width_unit_factor(2)


class Key225Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key225Unit, self).__init__()
        self.name = "u225"
        self.set_key_width_unit_factor(2.25)


class Key250Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key250Unit, self).__init__()
        self.name = "u250"
        self.set_key_width_unit_factor(2.5)


class Key275Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key275Unit, self).__init__()
        self.name = "u275"
        self.set_key_width_unit_factor(2.75)


class Key300Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key300Unit, self).__init__()
        self.name = "u300"
        self.set_key_width_unit_factor(3)


class Key400Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key400Unit, self).__init__()
        self.name = "u400"
        self.set_key_width_unit_factor(4)


class Key500Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key500Unit, self).__init__()
        self.name = "u500"
        self.set_key_width_unit_factor(5)


class Key600Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key600Unit, self).__init__()
        self.name = "u600"
        self.set_key_width_unit_factor(6)


class Key625Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key625Unit, self).__init__()
        self.name = "u625"
        self.set_key_width_unit_factor(6.25)


class Key700Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key700Unit, self).__init__()
        self.name = "u700"
        self.set_key_width_unit_factor(7)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
