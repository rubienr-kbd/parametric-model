from iso_keys import *
from utils import KeyUtils


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
            Key100UnitSpacerConnected()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_1(size: KeyboardSize) -> List[Key]:
    """
    zxcv row
    """
    r = [LeftShiftKey(),
         CharacterKey("|"),
         CharacterKey("y"),
         CharacterKey("x"),
         CharacterKey("c"),
         CharacterKey("v"),
         CharacterKey("b"),
         CharacterKey("n"),
         CharacterKey("m"),
         CharacterKey(","),
         CharacterKey("."),
         CharacterKey("-"),
         RightShiftKey()]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # arrow key
        r.extend([
            Key100UnitUpArrowSpacer(),
            ArrowUpKey(),
            Key100UnitSpacerFilled()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            CharacterKey("2"),
            CharacterKey("3"),
            IsoNumpadEnterKey()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_2(size: KeyboardSize) -> List[Key]:
    """
    asdf row
    """
    left_connected_spacer = Key125UnitSpacer()
    left_connected_spacer.base.is_connected_left = True
    r = [CapsLockKey(),
         CharacterKey("a"),
         CharacterKey("s"),
         CharacterKey("d"),
         CharacterKey("f"),
         CharacterKey("g"),
         CharacterKey("h"),
         CharacterKey("j"),
         CharacterKey("k"),
         CharacterKey("l"),
         CharacterKey("ö"),
         CharacterKey("ä"),
         CharacterKey("#"),
         left_connected_spacer]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S80.value:
        # empty
        r.extend([
            Key100UnitUpArrowSpacer(),
            Key100UnitSpacerFilled(),
            Key100UnitSpacerFilled()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacer(),
            CharacterKey("5"),
            CharacterKey("6"),
            Key100UnitSpacerConnected()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_row_3(size: KeyboardSize) -> List[Key]:
    """
    qwer row
    """
    r = [TabKey(),
         CharacterKey("q"),
         CharacterKey("w"),
         CharacterKey("e"),
         CharacterKey("r"),
         CharacterKey("t"),
         CharacterKey("z"),
         CharacterKey("u"),
         CharacterKey("i"),
         CharacterKey("o"),
         CharacterKey("p"),
         CharacterKey("ü"),
         CharacterKey("+"),
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
            CharacterKey("8"),
            CharacterKey("9"),
            IsoNumpadPlusKey()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def build_key_row_4(size: KeyboardSize) -> List[Key]:
    """
    number row
    """
    r = [CharacterKey("^"),
         CharacterKey("1"),
         CharacterKey("2"),
         CharacterKey("3"),
         CharacterKey("4"),
         CharacterKey("5"),
         CharacterKey("6"),
         CharacterKey("7"),
         CharacterKey("8"),
         CharacterKey("9"),
         CharacterKey("0"),
         CharacterKey("ß"),
         CharacterKey("´"),
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
            CharacterKey("/"),
            CharacterKey("*"),
            CharacterKey("-")])

    return r


def build_key_row_5(size: KeyboardSize) -> List[Key]:
    """
    F row
    """
    r = [EscapeKey(),
         F1Key(),
         CharacterKey("F2"),
         CharacterKey("F3"),
         F4Key(),
         F5Key(),
         CharacterKey("F6"),
         CharacterKey("F7"),
         F8Key(),
         F9Key(),
         CharacterKey("F10"),
         CharacterKey("F11"),
         F12Key()
         ]

    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    if size.value >= KeyboardSize.S40.value:
        # print, scroll lock, pause
        r.extend([
            PrintKey(),
            ScrollLockKey(),
            PauseKey()])

    if size.value >= KeyboardSize.S100.value:
        # numpad
        r.extend([
            Key100UnitNumpadSpacerFilled(),
            Key100UnitSpacerFilled(),
            Key100UnitSpacerFilled(),
            Key100UnitSpacerFilled()])

    return r


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def build_key_matrix() -> List[List[Key]]:
    """
    Builds a matrix with key objects placed in ISO manner.
    Note: The key's placements and cad objects are not computed.
    @return: matrix of key objects
    """
    print("compute key matrix ...")
    size = GlobalConfig.matrix.layout_size
    assert size not in [KeyboardSize.S40, KeyboardSize.S60, KeyboardSize.S65, KeyboardSize.S75]

    matrix = [
        build_key_row_0(size),
        build_key_row_1(size),
        build_key_row_2(size),
        build_key_row_3(size),
        build_key_row_4(size),
        build_key_row_5(size)
    ]
    print("compute key matrix: done")
    return matrix


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def compute_placement_and_cad_objects(key_matrix: List[List[Key]]) -> None:
    print("compute key placement and cad objects ...")
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

            # compute placement and cad components of the key
            key.compute()

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
    print("compute key placement and cad objects: done")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_key_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, int, int, Direction]]:
    """
    Specifies which keys and which faces are to be connected.
    @param key_matrix: pool of keys with pre-computed placement and cad objects
    """
    result = list()  # type: List[Tuple[int, int, Direction, int, int, Direction]]

    # connections in between neighbours in same row
    row_idx = 0
    for row in key_matrix:
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, len(row)))
        row_idx += 1

    # connections in between adjacent rows 0 to 1
    result.extend(((0, k, Direction.BACK, 1, k, Direction.FRONT) for k in range(0, 3)))  # LCTL to LALT
    result.extend(((0, k, Direction.BACK, 1, k + 6, Direction.FRONT) for k in range(4, 8)))  # RALT to RCTL
    result.extend(((0, k, Direction.BACK, 1, k + 5, Direction.FRONT) for k in range(8, 11)))  # LARR to numpad
    result.extend([(0, 11, Direction.BACK, 1, 13 + 4, Direction.FRONT)])  #
    result.extend([(0, 12, Direction.BACK, 1, 14 + 4, Direction.FRONT)])  #

    # connections in between adjacent rows 1 to 2
    result.extend(((1, k, Direction.BACK, 2, k, Direction.FRONT) for k in range(0, 13)))  # LSFT to RSFT
    result.extend(((1, k - 1, Direction.BACK, 2, k, Direction.FRONT) for k in range(14, len(key_matrix[2]))))  # spacer to numpad

    # connections in between adjacent rows 2 to 3
    result.extend(((2, k, Direction.BACK, 3, k, Direction.FRONT) for k in range(0, 13)))  # CSFT to #
    result.extend(((2, k, Direction.BACK, 3, k, Direction.FRONT) for k in range(14, len(key_matrix[2]))))  # spacer to numpad

    # connections in between adjacent rows 3 to 4
    result.extend(((3, k, Direction.BACK, 4, k, Direction.FRONT) for k in range(0, len(key_matrix[3]))))  # TAB to numpad

    # connections in between adjacent rows 4 to 5
    result.extend(((4, k, Direction.BACK, 5, k, Direction.FRONT) for k in range(0, len(key_matrix[5]))))  # ESC to F12
    result.extend([(4, len(key_matrix[5]), Direction.BACK, 5, len(key_matrix[5]) - 1, Direction.FRONT)])  # ESC to F12

    return result


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_connector_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, Direction, int, int, Direction, Direction]]:
    """
    Specifies which key-connectors from :func:`iso_matrix.get_key_connection_mapping` and which faces are to be connected.
    @param key_matrix: pool of keys with pre-computed placement and cad objects
    """
    result = list()  # type: List[Tuple[int, int, Direction,  Direction, int, int, Direction,  Direction]]

    # rows 0 to 1
    result.extend(((0, k, Direction.RIGHT, Direction.BACK, 1, k, Direction.RIGHT, Direction.FRONT) for k in range(0, 4)))  # LCTL to LALT
    result.extend(((0, k, Direction.RIGHT, Direction.BACK, 1, k + 6, Direction.RIGHT, Direction.FRONT) for k in range(4, 8)))  # RALT to RCTL
    result.extend(((0, k, Direction.RIGHT, Direction.BACK, 1, k + 5, Direction.RIGHT, Direction.FRONT) for k in range(8, 11)))  # RALT to RCTL

    # rows 1 to 2
    result.extend(((1, k, Direction.RIGHT, Direction.BACK, 2, k, Direction.RIGHT, Direction.FRONT) for k in range(0, 12)))  # LSFT to RSFT
    result.extend(((1, k, Direction.RIGHT, Direction.BACK, 2, k + 1, Direction.RIGHT, Direction.FRONT) for k in range(13, len(key_matrix[2]) - 1)))  # spacer to numpad

    # rows 2 to 3
    result.extend(((2, k, Direction.RIGHT, Direction.BACK, 3, k, Direction.RIGHT, Direction.FRONT) for k in range(0, 12)))  # CSFT to #
    result.extend(((2, k, Direction.RIGHT, Direction.BACK, 3, k, Direction.RIGHT, Direction.FRONT) for k in range(13, len(key_matrix[2]) - 1)))  # spacer to numpad

    # rows 3 to 4
    result.extend(((3, k, Direction.RIGHT, Direction.BACK, 4, k, Direction.RIGHT, Direction.FRONT) for k in range(0, len(key_matrix[3]) - 1)))  # TAB to numpad

    # rows 4 to 5
    result.extend(((4, k, Direction.RIGHT, Direction.BACK, 5, k, Direction.RIGHT, Direction.FRONT) for k in range(0, len(key_matrix[5]) - 1)))  # ESC to F12

    return result
