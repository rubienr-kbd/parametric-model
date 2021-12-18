from typing import List, Optional
from cadquery import Shape
from config import *
from key_mixins import *

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


class KeyBase(KeyPlane, Computeable, CadObject, KeyBaseMixin):
    def __init__(self, config: KeyBaseConfig) -> None:
        super(KeyBase, self).__init__()
        self.unit_length = config.unit_length  # type: float
        self.unit_width_factor = 1.0  # type: float
        self.unit_depth_factor = 1.0  # type: float
        self.clearance_left = config.clearance_x  # type: float
        self.clearance_right = config.clearance_x  # type: float
        self.clearance_top = config.clearance_y  # type: float
        self.clearance_bottom = config.clearance_y  # type: float
        self.is_visible = True  # type: bool

    def update(self) -> None:
        self.width = self.unit_width_factor * self.unit_length
        self.depth = self.unit_depth_factor * self.unit_length


class KeyCap(KeyBox, Computeable, CadObject):
    def __init__(self, config: KeyCapConfig) -> None:
        super(KeyCap, self).__init__()
        self.unit_width_factor = 1.0  # type: float
        self.unit_depth_factor = 1.0  # type: float
        self.width_clearance = config.width_clearance  # type: float
        self.depth_clearance = config.depth_clearance  # type: float
        self.width = 0.0  # type: float
        self.depth = 0.0  # type: float
        self.thickness = config.thickness  # type: float
        self.z_clearance = config.z_clearance  # type: float
        self.dish_inset = config.dish_inset  # type: float

    def update(self) -> None:
        self.width = self.unit_width_factor * GlobalConfig.key_base.unit_length - self.width_clearance
        self.depth = self.unit_depth_factor * GlobalConfig.key_base.unit_length - self.depth_clearance

    def compute(self) -> None:
        self._cad_object = cadquery.Workplane() \
            .wedge(self.width,
                   self.thickness,
                   self.depth,
                   1,
                   1,
                   self.width - 1,
                   self.depth - 1,
                   centered=[True, False, True]) \
            .rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, self.z_clearance))


class KeySwitch(KeyBox, Computeable, CadObject):
    def __init__(self, config: KeySwitchConfig) -> None:
        super(KeySwitch, self).__init__()
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class KeySwitchSlot(KeyBox, Computeable, CadObject):
    def __init__(self, config: KeySwitchSlotConfig) -> None:
        super(KeySwitchSlot, self).__init__()
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


class CadObjects(object):
    def __init__(self):
        self.plane = None  # type: Optional[Shape]
        self.key_name = None  # type: Optional[Shape]
        self.key_cap = None  # type: Optional[Shape]
        self.switch = None  # type: Optional[Shape]
        self.slot = None  # type: Optional[Shape]


class Key(Computeable, CadKeyMixin):
    def __init__(self) -> None:
        self.key_base = KeyBase(GlobalConfig.key_base)
        self.cap = KeyCap(GlobalConfig.cap)
        self.switch = KeySwitch(GlobalConfig.switch)
        self.switch_slot = KeySwitch(GlobalConfig.switch_slot)
        self.cad_objects = CadObjects()
        self.name = ""

    def update(self):
        self.key_base.update()
        self.cap.update()
        self.switch.update()
        self.switch_slot.update()

    def compute(self):
        self.key_base.compute()
        self.post_compute_cad_key_base()
        self.cad_objects.plane = self.key_base.get_cad_object()

        self.cad_objects.key_name = self.post_compute_key_base_name()

        self.cap.compute()
        self.post_compute_cad_cap()
        self.cad_objects.key_cap = self.cap.get_cad_object()

        self.switch.compute()
        self.post_compute_cad_switch()
        self.cad_objects.switch = self.switch.get_cad_object()

        self.switch_slot.compute()
        self.post_compute_cad_switch_slot()
        self.cad_objects.slot = self.switch_slot.get_cad_object()

    def set_unit_width_factor(self, factor: float) -> None:
        self.key_base.unit_width_factor = factor
        self.cap.unit_width_factor = factor

    def set_unit_depth_factor(self, factor: float) -> None:
        self.key_base.unit_depth_factor = factor
        self.cap.unit_depth_factor = factor


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Key100Unit(Key):
    def __init__(self) -> None:
        super(Key100Unit, self).__init__()
        self.name = "u100"


class Key100UnitSpacer(Key):
    def __init__(self) -> None:
        super(Key100UnitSpacer, self).__init__()
        self.name = "su100"
        self.key_base.is_visible = False


class Key125UnitSpacer(Key):
    def __init__(self) -> None:
        super(Key125UnitSpacer, self).__init__()
        self.name = "su125"
        self.set_unit_width_factor(1.25)
        self.key_base.is_visible = False


class Key125Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key125Unit, self).__init__()
        self.name = "u125"
        self.set_unit_width_factor(1.25)


class Key150Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key150Unit, self).__init__()
        self.name = "u150"
        self.set_unit_width_factor(1.5)


class Key175Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key175Unit, self).__init__()
        self.name = "u175"
        self.set_unit_width_factor(1.75)


class Key200Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key200Unit, self).__init__()
        self.name = "u200"
        self.set_unit_width_factor(2)


class Key225Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key225Unit, self).__init__()
        self.name = "u225"
        self.set_unit_width_factor(2.25)


class Key250Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key250Unit, self).__init__()
        self.name = "u250"
        self.set_unit_width_factor(2.5)


class Key275Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key275Unit, self).__init__()
        self.name = "u275"
        self.set_unit_width_factor(2.75)


class Key300Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key300Unit, self).__init__()
        self.name = "u300"
        self.set_unit_width_factor(3)


class Key400Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key400Unit, self).__init__()
        self.name = "u400"
        self.set_unit_width_factor(4)


class Key500Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key500Unit, self).__init__()
        self.name = "u500"
        self.set_unit_width_factor(5)


class Key600Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key600Unit, self).__init__()
        self.name = "u600"
        self.set_unit_width_factor(6)


class Key625Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key625Unit, self).__init__()
        self.name = "u625"
        self.set_unit_width_factor(6.25)


class Key700Unit(Key100Unit):
    def __init__(self) -> None:
        super(Key700Unit, self).__init__()
        self.name = "u700"
        self.set_unit_width_factor(7)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
