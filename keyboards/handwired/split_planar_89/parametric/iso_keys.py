from types import MethodType

from default_keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# default ISO keys
# https://deskthority.net/wiki/Keycap_size_by_keyboard
# https://deskthority.net/wiki/Unit


class CharacterKey(Key100Unit):
    def __init__(self, name="ch"):
        super(CharacterKey, self).__init__()
        self.name = name


class TabKey(Key150Unit):
    def __init__(self):
        super(TabKey, self).__init__()
        self.name = "TAB"


class CapsLockKey(Key175Unit):
    def __init__(self):
        super(CapsLockKey, self).__init__()
        self.name = "CSFT"


class LeftAltKey(Key125Unit):
    def __init__(self):
        super(LeftAltKey, self).__init__()
        self.name = "LALT"


class LeftCtrlKey(Key125Unit):
    def __init__(self):
        super(LeftCtrlKey, self).__init__()
        self.name = "LCTR"


class RightAltKey(Key125Unit):
    def __init__(self):
        super(RightAltKey, self).__init__()
        self.name = "RALT"


class FnKey(Key125Unit):
    def __init__(self):
        super(FnKey, self).__init__()
        self.name = "FN"


class RightCtrlKey(Key125Unit):
    def __init__(self):
        super(RightCtrlKey, self).__init__()
        self.name = "RCTL"


class LeftShiftKey(Key125Unit):
    def __init__(self):
        super(LeftShiftKey, self).__init__()
        self.name = "LSFT"


class RightShiftKey(Key275Unit):
    def __init__(self):
        super(RightShiftKey, self).__init__()
        self.name = "RSFT"


class LeftOsKey(Key125Unit):
    def __init__(self):
        super(LeftOsKey, self).__init__()
        self.name = "LOS"


class RightMenulKey(Key125Unit):
    def __init__(self):
        super(RightMenulKey, self).__init__()
        self.name = "MENU"


class SpaceKey(Key625Unit):
    def __init__(self):
        super(SpaceKey, self).__init__()
        self.name = "SPC"


class BackspaceKey(Key200Unit):
    def __init__(self):
        super(BackspaceKey, self).__init__()
        self.name = "BSP"


class ScrollLockKey(Key100Unit):
    def __init__(self):
        super(ScrollLockKey, self).__init__()
        self.name = "SRL"


class PauseKey(Key100Unit):
    def __init__(self):
        super(PauseKey, self).__init__()
        self.name = "PAU"


class HomeKey(Key100Unit):
    def __init__(self):
        super(HomeKey, self).__init__()
        self.name = "HOM"


class EndKey(Key100Unit):
    def __init__(self):
        super(EndKey, self).__init__()
        self.name = "END"


class PageUpKey(Key100Unit):
    def __init__(self):
        super(PageUpKey, self).__init__()
        self.name = "PUP"


class PageDown(Key100Unit):
    def __init__(self):
        super(PageDown, self).__init__()
        self.name = "PDN"


class IsoEnterKey(Key150Unit):
    """
       ↓ 1.5 unit
    ╭─────╮
    │  ↲  │
    ╰╮    │ ← 2 units
     │    │
     ╰────╯
        ↑ 1.25
    """

    def __init__(self):
        super(IsoEnterKey, self).__init__()
        self.name = "ENT"
        self.base.unit_depth_factor = 2
        self.base.position_offset = [0, - GlobalConfig.key_base.unit_length / 2, 0]

        def compute(self, outer_self=self, *args, **kwargs) -> None:

            upper_part = cadquery.Workplane() \
                .wedge(self.width,
                       self.thickness,
                       outer_self.base.unit_length - self.depth_clearance,
                       self.dish_inset,
                       self.dish_inset,
                       self.width - self.dish_inset,
                       outer_self.base.unit_length - self.depth_clearance - self.dish_inset,
                       centered=(True, False, True)) \
                .rotate((0, 0, 0), (1, 0, 0), 90) \
                .translate((0, outer_self.base.unit_length / 2, self.z_clearance)) \

            lower_part = cadquery.Workplane() \
                .wedge(outer_self.base.unit_length * 1.25 - self.depth_clearance,
                       self.thickness,
                       outer_self.base.unit_length,
                       self.dish_inset,
                       - self.dish_inset,
                       outer_self.base.unit_length * 1.25 - self.depth_clearance - self.dish_inset,
                       outer_self.base.unit_length - self.dish_inset,
                       centered=(True, False, False)) \
                .rotate((0, 0, 0), (1, 0, 0), 90) \
                .translate(((2 - 1.25) / 2 * (outer_self.base.unit_length - self.width_clearance / 2) / 2 - self.width_clearance / 2,
                            self.depth_clearance / 2,
                            self.z_clearance)) \

            self._cad_object = upper_part.union(lower_part)

        self.cap.compute = MethodType(compute, self.cap)


class IsoNumpadEnterKey(Key100Unit):
    """
      ↓ 1 unit
    ╭───╮
    │   │
    │ ↲ │  ← 2 units
    │   │
    ╰───╯
    """

    def __init__(self):
        super(IsoNumpadEnterKey, self).__init__()
        self.name = "NENT"
        self.base.unit_depth_factor = 2
        self.base.position_offset = [0, - GlobalConfig.key_base.unit_length / 2, 0]


class IsoNumpadPlusKey(Key100Unit):
    """
      ↓ 1 unit
    ╭───╮
    │   │
    │ + │  ← 2 units
    │   │
    ╰───╯
    """

    def __init__(self):
        super(IsoNumpadPlusKey, self).__init__()
        self.name = "NPLU"
        self.base.unit_depth_factor = 2
        self.base.position_offset = [0, - GlobalConfig.key_base.unit_length / 2, 0]


class IsoNumpadInsKey(Key200Unit):
    """
          ↓ 2 unitsy
    ╭──────────╮
    │  0 INS   │ ← 1 unit
    ╰──────────╯
    """

    def __init__(self):
        super(IsoNumpadInsKey, self).__init__()
        self.name = "NINS"
        self.base.clearance_left = GlobalConfig.group.clearance_x_numpad


class ArrowDownKey(CharacterKey):
    def __init__(self):
        super(ArrowDownKey, self).__init__()
        self.name = "DAR"


class ArrowRightKey(CharacterKey):
    def __init__(self):
        super(ArrowRightKey, self).__init__()
        self.name = "RAR"


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# keys with special clearance

class EscapeKey(CharacterKey):
    """
    for spacing ESC
      ╭───╮
      │ESC│ →
      ╰───╯
    """

    def __init__(self):
        super(EscapeKey, self).__init__()
        self.name = "ESC"
        self.base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2
        self.base.clearance_bottom = GlobalConfig.group.clearance_y_f_group / 2


class F1Key(CharacterKey):
    """
    for spacing F1
      ╭───╮
    ← │F1 │
      ╰───╯
    """

    def __init__(self):
        super(F1Key, self).__init__()
        self.name = "F1"
        self.base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


class F4Key(CharacterKey):
    """
    for spacing F4
      ╭───╮
      │F4 │ →
      ╰───╯
    """

    def __init__(self):
        super(F4Key, self).__init__()
        self.name = "F4"
        self.base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


class F5Key(CharacterKey):
    """
    for spacing F5
      ╭───╮
    ← │F5 │
      ╰───╯
    """

    def __init__(self):
        super(F5Key, self).__init__()
        self.name = "F5"
        self.base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


class F8Key(CharacterKey):
    """
    for spacing F8
      ╭───╮
      │F8 │ →
      ╰───╯
    """

    def __init__(self):
        super(F8Key, self).__init__()
        self.name = "F8"
        self.base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


class F9Key(CharacterKey):
    """
    for spacing F9
      ╭───╮
    ← │F9 │
      ╰───╯
    """

    def __init__(self):
        super(F9Key, self).__init__()
        self.name = "F9"
        self.base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


class F12Key(CharacterKey):
    def __init__(self):
        super(F12Key, self).__init__()
        self.name = "F12"


class PrintKey(CharacterKey):
    """
    spacing
      ╭───╮
    ← │PRT│
      ╰───╯
    """

    def __init__(self):
        super(PrintKey, self).__init__()
        self.name = "PRT"
        self.base.clearance_left = GlobalConfig.group.clearance_x_arrow_group


class InsertKey(CharacterKey):
    """
    spacing
      ╭───╮
    ← │INS│
      ╰───╯
    """

    def __init__(self):
        super(InsertKey, self).__init__()
        self.name = "INS"
        self.base.clearance_left = GlobalConfig.group.clearance_x_arrow_group


class DeleteKey(CharacterKey):
    """
    spacing
      ╭───╮
    ← │DEL│
      ╰───╯
    """

    def __init__(self):
        super(DeleteKey, self).__init__()
        self.name = "DEL"
        self.base.clearance_left = GlobalConfig.group.clearance_x_arrow_group


class NumpadDeleteKey(CharacterKey):
    def __init__(self):
        super(NumpadDeleteKey, self).__init__()
        self.name = "NDEL"


class ArrowLeftKey(CharacterKey):
    def __init__(self):
        super(ArrowLeftKey, self).__init__()
        self.name = "LAR"
        self.base.clearance_left = GlobalConfig.group.clearance_x_arrow_group


class ArrowUpKey(CharacterKey):
    def __init__(self):
        super(ArrowUpKey, self).__init__()
        self.name = "UAR"
        self.clearance_left = \
            GlobalConfig.group.clearance_x_f_group + GlobalConfig.key_base.clearance_x + \
            GlobalConfig.key_base.clearance_x + GlobalConfig.key_base.unit_length + GlobalConfig.key_base.unit_length / 2


class Key100UnitNumpadSpacer(Key):
    """
    for spacing the numpad
      ╭───╮
    ← │num│
      ╰───╯
    """

    def __init__(self) -> None:
        super(Key100UnitNumpadSpacer, self).__init__()
        self.name = "sn100"
        self.base.clearance_left = GlobalConfig.group.clearance_x_numpad


class Key100UnitNumpadSpacerFilled(Key100UnitNumpadSpacer):
    """
    for spacing the filled key above numpad
      ╭───╮
    ← │   │
      ╰───╯
      ╭───╮
      │num│
      ╰───╯
    """

    def __init__(self) -> None:
        super(Key100UnitNumpadSpacerFilled, self).__init__()
        self.name = "sf100"
        self.base.is_visible = True
        self.base.is_filled = True
        self.base.is_connected = True

class Key100UnitUpArrowSpacer(Key100UnitSpacer):
    """
    for spacing the arrow-up key
      ╭───╮ ╭───╮
    ← │spc│ │ ↑ │
      ╰───╯ ╰───╯
      ╭───╮ ╭───╮ ╭───╮
      │ ← │ │ ↓ │ │ → │
      ╰───╯ ╰───╯ ╰───╯
    """

    def __init__(self) -> None:
        super(Key100UnitUpArrowSpacer, self).__init__()
        self.name = "sa100"
        self.base.clearance_left = GlobalConfig.group.clearance_x_arrow_group
        self.base.is_visible = True
        self.base.is_filled = True
        self.base.is_connected = True
