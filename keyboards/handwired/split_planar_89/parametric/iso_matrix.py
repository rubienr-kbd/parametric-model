from iso_keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_0(size: KeyboardSize):
    """
    space bar row
    """
    r = [
        LeftCtrlKey(),
        LeftMenulKey(),
        LeftAltKey(),
        SpaceKey(),
        RightAltKey(),
        RightContextMenulKey(),
        RightCtrlKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # arrow key group
        r.extend([
            ArrowLeftKey(),
            ArrowDownKey(),
            ArrowRightKey()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            IsoNumpadInsKey(),
            NumpadDeleteKey(),
            Key100UnitSpacer()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_1(size: KeyboardSize):
    """
    zxcv row
    """
    r = [LeftShiftKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         RightShiftKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # arrow key
        r.extend([
            Key100UnitUpArrowSpacer(),
            ArrowUpKey(),
            Key100UnitSpacer()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            Key100Unit(),
            Key100Unit(),
            IsoNumpadEnterKey()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_2(size: KeyboardSize):
    """
    asdf row
    """
    r = [CapsLockKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         Key100UnitSpacer()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # empty
        r.extend([
            Key100UnitUpArrowSpacer(),
            Key100UnitSpacer(),
            Key100UnitSpacer()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            Key100Unit(),
            Key100Unit(),
            Key100UnitSpacer()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_3(size: KeyboardSize):
    """
    qwer row
    """
    r = [TabKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # ins/del 6-key block
        r.extend([
            IsoEnterKey(),
            DeleteKey(),
            EndKey(),
            PageDown()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            Key100Unit(),
            Key100Unit(),
            IsoNumpadPlusKey()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def build_key_row_4(size: KeyboardSize):
    """
    number row
    """
    r = [CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         BackspaceKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # ins/del 6-key block
        r.extend([
            InsertKey(),
            HomeKey(),
            PageUpKey()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            Key100Unit(),
            Key100Unit(),
            Key100Unit()])

    return r


def build_key_row_5(size: KeyboardSize):
    """
    F row
    """
    r = [EscapeKey(),
         F1Key(),
         CharacterKey(),
         CharacterKey(),
         F4Key(),
         F5Key(),
         CharacterKey(),
         CharacterKey(),
         F8Key(),
         F9Key(),
         CharacterKey(),
         CharacterKey(),
         F12Key()
         ]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S40.value:
        # print, scroll lock, pause
        r.extend([
            PrintKey(),
            ScrollLockKey(),
            PauseKey()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_keyboard_matrix():
    size = GlobalConfig.matrix.layout_size
    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    return [
        build_key_row_0(size),
        build_key_row_1(size),
        build_key_row_2(size),
        build_key_row_3(size),
        build_key_row_4(size),
        build_key_row_5(size)
    ]
