from iso_keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_0(size: KeyboardSize = KeyboardSize.S100):
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
        RightCtrlKey(),
        ArrowLeftKey(),
        ArrowDownKey(),
        ArrowRightKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # arrow key group
        r.extend([
            ArrowLeftKey(),
            ArrowDownKey(),
            ArrowRightKey()])

    if size == KeyboardSize.S100:
        # numpad
        r.extend([
            Key200Unit(),
            DeleteKey()])

    KeyUtils.update_key_pos_in_row(r)
    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_1(size: KeyboardSize = KeyboardSize.S100):
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

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # arrow key
        r.extend([
            Key100UnitUpArrowSpacer(),
            ArrowUpKey(),
            Key100UnitSpacer()])

    if size == KeyboardSize.S100:
        # numpad
        r.extend([
            Key100Unit(),
            Key100Unit(),
            Key100Unit(),
            IsoNumpadEnterKey()])

    KeyUtils.update_key_pos_in_row(r)
    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_2(size: KeyboardSize = KeyboardSize.S100):
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

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # empty
        r.extend([
            Key100UnitUpArrowSpacer(),
            Key100UnitSpacer(),
            Key100UnitSpacer()])

    if size == KeyboardSize.S100:
        # numpad
        r.extend([
            Key100Unit(),
            Key100Unit(),
            Key100Unit(),
            Key100UnitSpacer()])

    KeyUtils.update_key_pos_in_row(r)
    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_3(size: KeyboardSize = KeyboardSize.S100):
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

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # ins/del 6-key block
        r.extend([
            IsoEnterKey(),
            DeleteKey(),
            EndKey(),
            PageDown()])

    if size == KeyboardSize.S100:
        # numpad
        r.extend([
            Key100Unit(),
            Key100Unit(),
            Key100Unit(),
            IsoNumpadPlusKey()])

    KeyUtils.update_key_pos_in_row(r)
    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def build_key_row_4(size: KeyboardSize = KeyboardSize.S100):
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

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # ins/del 6-key block
        r.extend([
            InsertKey(),
            HomeKey(),
            PageUpKey()])

    if size == KeyboardSize.S100:
        # numpad
        r.extend([
            Key100Unit(),
            Key100Unit(),
            Key100Unit(),
            Key100Unit()])

    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_5(size: KeyboardSize = KeyboardSize.S100):
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
         F12Key(), ]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75, KeyboardSize.S65]

    if size == KeyboardSize.S80:
        # print, scroll lock, pause
        r.extend([
            PrintKey(),
            ScrollLockKey(),
            PauseKey()])

    KeyUtils.update_key_pos_in_row(r)
    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_keyboard_matrix():
    if GlobalConfig.matrix.layout_size == KeyboardSize.S100:
        return [
            build_key_row_0(KeyboardSize.S100),
            build_key_row_1(KeyboardSize.S100),
            build_key_row_2(KeyboardSize.S100),
            build_key_row_3(KeyboardSize.S100),
            build_key_row_4(KeyboardSize.S100),
            build_key_row_5(KeyboardSize.S100)]

    elif GlobalConfig.matrix.layout_size == KeyboardSize.S80:
        return [
            build_key_row_0(KeyboardSize.S80),
            build_key_row_1(KeyboardSize.S80),
            build_key_row_2(KeyboardSize.S80),
            build_key_row_3(KeyboardSize.S80),
            build_key_row_4(KeyboardSize.S80),
            build_key_row_5(KeyboardSize.S80)]
    else:
        assert False
