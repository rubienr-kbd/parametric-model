from keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# default ISO keys

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


class LeftAltKey(Key125Unit):
    def __init__(self):
        self.name = "LALT"
        super(LeftAltKey, self).__init__()


class LeftCtrlKey(Key125Unit):
    def __init__(self):
        self.name = "LCTR"
        super(LeftCtrlKey, self).__init__()


class RightAltKey(Key125Unit):
    def __init__(self):
        self.name = "RALT"
        super(RightAltKey, self).__init__()


class RightCtrlKey(Key125Unit):
    def __init__(self):
        self.name = "RCTL"
        super(RightCtrlKey, self).__init__()


class LeftShiftKey(Key125Unit):
    def __init__(self):
        self.name = "LSFT"
        super(LeftShiftKey, self).__init__()


class RightShiftKey(Key225Unit):
    def __init__(self):
        self.name = "RSFT"
        super(RightShiftKey, self).__init__()


class LeftMenulKey(Key125Unit):
    def __init__(self):
        self.name = "LMEN"
        super(LeftMenulKey, self).__init__()


class RightContextMenulKey(Key125Unit):
    def __init__(self):
        self.name = "RCTX"
        super(RightContextMenulKey, self).__init__()


class SpaceKey(Key566Unit):
    def __init__(self):
        self.name = "SPC"
        super(SpaceKey, self).__init__()


class BackspaceKey(Key175Unit):
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


class IsoEnterKey(Key111Unit):
    def __init__(self):
        self.name = "ENT"
        super(IsoEnterKey, self).__init__()

class ArrowLeftKey(CharacterKey):
    def __init__(self):
        super(ArrowLeftKey, self).__init__()
        self.name = "LAR"

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
    def __init__(self):
        super(EscapeKey, self).__init__()
        self.name = "ESC"
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class F1Key(CharacterKey):
    def __init__(self):
        super(F1Key, self).__init__()
        self.name = "F1"
        self.clearance_left = GlobalConfig.f_group.clearance_x / 2


class F4Key(CharacterKey):
    def __init__(self):
        super(F4Key, self).__init__()
        self.name = "F4"
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class F5Key(CharacterKey):
    def __init__(self):
        super(F5Key, self).__init__()
        self.name = "F5"
        self.clearance_left = GlobalConfig.f_group.clearance_x / 2


class F8Key(CharacterKey):
    def __init__(self):
        super(F8Key, self).__init__()
        self.name = "F8"
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class F9Key(CharacterKey):
    def __init__(self):
        super(F9Key, self).__init__()
        self.name = "F9"
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class F12Key(CharacterKey):
    def __init__(self):
        super(F12Key, self).__init__()
        self.name = "F12"
        self.clearance_left = GlobalConfig.f_group.clearance_x / 2
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class PrintKey(CharacterKey):
    def __init__(self):
        super(PrintKey, self).__init__()
        self.name = "PRT"
        self.clearance_left = GlobalConfig.f_group.clearance_x / 2
        self.clearance_right = GlobalConfig.f_group.clearance_x / 2


class InsertKey(CharacterKey):
    def __init__(self):
        super(InsertKey, self).__init__()
        self.name = "INS"
        self.clearance_left = GlobalConfig.f_group.clearance_x


class DeleteKey(CharacterKey):
    def __init__(self):
        super(DeleteKey, self).__init__()
        self.name = "DEL"
        self.clearance_left = GlobalConfig.f_group.clearance_x


class ArrowLeftKey(CharacterKey):
    def __init__(self):
        super(ArrowLeftKey, self).__init__()
        self.name = "RAR"
        self.clearance_left = GlobalConfig.f_group.clearance_x


class ArrowUpKey(CharacterKey):
    def __init__(self):
        super(ArrowUpKey, self).__init__()
        self.name = "UAR"
        self.clearance_left = GlobalConfig.f_group.clearance_x + GlobalConfig.key_base.clearance_x + \
                              GlobalConfig.key_base.clearance_x + GlobalConfig.key_base.unit_length + GlobalConfig.key_base.unit_length / 2
