from keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# default ISO keys
# https://deskthority.net/wiki/Keycap_size_by_keyboard


class CharacterKey(Key100Unit):
    def __init__(self):
        self.name = "char"
        super(CharacterKey, self).__init__()


class TabKey(Key150Unit):
    def __init__(self):
        self.name = "TAB"
        super(TabKey, self).__init__()


class CapsLockKey(Key175Unit):
    def __init__(self):
        self.name = "CSFT"
        super(CapsLockKey, self).__init__()


class LeftAltKey(Key150Unit):
    def __init__(self):
        self.name = "LALT"
        super(LeftAltKey, self).__init__()


class LeftCtrlKey(Key150Unit):
    def __init__(self):
        self.name = "LCTR"
        super(LeftCtrlKey, self).__init__()


class RightAltKey(Key150Unit):
    def __init__(self):
        self.name = "RALT"
        super(RightAltKey, self).__init__()


class RightCtrlKey(Key150Unit):
    def __init__(self):
        self.name = "RCTL"
        super(RightCtrlKey, self).__init__()


class LeftShiftKey(Key150Unit):
    def __init__(self):
        self.name = "LSFT"
        super(LeftShiftKey, self).__init__()


class RightShiftKey(Key275Unit):
    def __init__(self):
        self.name = "RSFT"
        super(RightShiftKey, self).__init__()


class LeftMenulKey(Key125Unit):
    def __init__(self):
        self.name = "LMEN"
        super(LeftMenulKey, self).__init__()


class FnKey(Key125Unit):
    def __init__(self):
        self.name = "FN"
        super(FnKey, self).__init__()


class RightContextMenulKey(Key125Unit):
    def __init__(self):
        self.name = "RCTX"
        super(RightContextMenulKey, self).__init__()


class SpaceKey(Key625Unit):
    def __init__(self):
        self.name = "SPC"
        super(SpaceKey, self).__init__()


class BackspaceKey(Key200Unit):
    def __init__(self):
        self.name = "BSP"
        super(BackspaceKey, self).__init__()


class ScrollLockKey(Key100Unit):
    def __init__(self):
        self.name = "SRL"
        super(ScrollLockKey, self).__init__()


class PauseKey(Key100Unit):
    def __init__(self):
        self.name = "PAU"
        super(PauseKey, self).__init__()


class HomeKey(Key100Unit):
    def __init__(self):
        self.name = "HOM"
        super(HomeKey, self).__init__()


class EndKey(Key100Unit):
    def __init__(self):
        self.name = "END"
        super(EndKey, self).__init__()


class PageUpKey(Key100Unit):
    def __init__(self):
        self.name = "PUP"
        super(PageUpKey, self).__init__()


class PageDown(Key100Unit):
    def __init__(self):
        self.name = "PDN"
        super(PageDown, self).__init__()


class IsoEnterKey(Key150Unit):
    """
       ↓ 1.5 unit
    ╭─────╮
    │     │
    ╰╮    │ ← 2 units
     │    │
     ╰────╯
        ↑ 1.25
    """
    def __init__(self):
        self.name = "ENT"
        super(IsoEnterKey, self).__init__()
        self.set_key_depth_unit_factor(2)


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
        self.name = "NENT"
        super(IsoNumpadEnterKey, self).__init__()
        self.set_key_depth_unit_factor(2)


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
        self.name = "NPLUS"
        super(IsoNumpadPlusKey, self).__init__()
        self.set_key_depth_unit_factor(2)


class IsoNumpadInsKey(Key200Unit):
    """
          ↓ 2 unitsy
    ╭──────────╮
    │  0 INS   │ ← 1 unit
    ╰──────────╯
    """
    def __init__(self):
        self.name = "NINS"
        super(IsoNumpadInsKey, self).__init__()


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
        self.key_base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


class F12Key(CharacterKey):
    def __init__(self):
        super(F12Key, self).__init__()
        self.name = "F12"
        self.key_base.clearance_right = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group / 2


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group


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
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group


class NumpadDeleteKey(CharacterKey):
    def __init__(self):
        super(NumpadDeleteKey, self).__init__()
        self.name = "NDEL"


class ArrowLeftKey(CharacterKey):
    def __init__(self):
        super(ArrowLeftKey, self).__init__()
        self.name = "RAR"
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group


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
        self.name = "ns100"
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group


class Key100UnitUpArrowSpacer(Key100UnitSpacer):
    """
    for spacing the arrow-up key
      ╭───╮ ╭───╮
      │spc│ │ ↑ │
      ╰───╯ ╰───╯
    """

    def __init__(self) -> None:
        super(Key100UnitUpArrowSpacer, self).__init__()
        self.name = "as100"
        self.key_base.clearance_left = GlobalConfig.group.clearance_x_f_group
