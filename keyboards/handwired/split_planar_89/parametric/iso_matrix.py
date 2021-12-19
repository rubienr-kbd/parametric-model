from iso_keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from utils import KeyUtils


def build_key_row_0(size: KeyboardSize) -> List[Key]:
    """
    space bar row
    """
    r = [
        LeftCtrlKey(),
        LeftOsKey(),
        LeftAltKey(),
        SpaceKey(),
        RightAltKey(),
        FnKey(),
        RightMenulKey(),
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


def build_key_row_1(size: KeyboardSize) -> List[Key]:
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


def build_key_row_2(size: KeyboardSize) -> List[Key]:
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
         Key125UnitSpacer()]

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


def build_key_row_3(size: KeyboardSize) -> List[Key]:
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
         CharacterKey(),
         IsoEnterKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # ins/del 6-key block
        r.extend([
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

def build_key_row_4(size: KeyboardSize) -> List[Key]:
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


def build_key_row_5(size: KeyboardSize) -> List[Key]:
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


def build_key_matrix() -> List[List[Key]]:
    """
    Builds a matrix with key objects placed in ISO manner.
    Note: The key's placements and cad objects are not computed.
    @return: matrix of key objects
    """
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


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def construct_key_placement(key_matrix: List[List[Key]]) -> List[Tuple[Key, CadObjects]]:
    objects = []  # type: List[Tuple[Key, CadObjects]]

    last_row = None
    last_key = None
    row_idx = 0

    for row in key_matrix:

        print("row {}".format(row_idx))
        print("  col│x       y     z   │key   unit│clrto clrri clrbo clrle│capwi  capde capth│vis")
        print("  ───┼──────────────────┼──────────┼───────────────────────┼──────────────────┼───")
        is_first_key_in_row = True
        col_idx = 0

        for key in row:
            # update/resolve input parameters dependencies
            key.update()

            # compute planar key placement in ISO style
            if is_first_key_in_row:
                if last_row is not None:
                    KeyUtils.set_position_relative_to(key.base, last_row[0].base, Direction.TOP)
                key.base.align_to_position(0, Direction.LEFT)
            elif last_key is not None:
                KeyUtils.set_position_relative_to(key.base, last_key.base, Direction.RIGHT)
            is_first_key_in_row = False
            last_key = key

            # compute cad objects
            key.compute()
            objects.append((key, key.cad_objects))

            print("  {col:2} │{x:6.2f}{y:6.2f}{z:6.2f}│{key:5} {unit:4.2f}│{clrto:5.2f} {clrri:5.2f} {clrbo:5.2f} {clrle:5.2f}│{capwi:6.2f} {capde:5.2f} {capth:5.2f}│{vis}"
                  .format(col=col_idx,
                          x=key.base.position[0], y=key.base.position[1], z=key.base.position[2],
                          key=key.name,
                          unit=key.base.unit_width_factor,
                          clrto=key.base.clearance_top,
                          clrri=key.base.clearance_right,
                          clrbo=key.base.clearance_bottom,
                          clrle=key.base.clearance_left,
                          capwi=key.cap.width,
                          capde=key.cap.depth,
                          capth=key.cap.thickness,
                          vis="yes" if key.base.is_visible else "no "))

            col_idx = col_idx + 1
        last_row = row
        row_idx = row_idx + 1
    return objects
