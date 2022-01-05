from cadquery import NearestToPointSelector

from src.iso_keys.keys import *
from src.cli_args import cli_args
from src.keys.canonical_keys import Key100UnitSpacerConnected, Key100UnitSpacerFilled, Key125UnitSpacer
from src.keys.key import Key
from src.keys.key_mixins import Direction
from src.keyboard_size import KeyboardSize

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from src.keys.utils import KeyUtils


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
    size = cli_args().keyboard_size
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

def get_key_face_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, int, int, Direction]]:
    """
    Specifies which keys and which keys' face are to be connected.
    @param key_matrix: pool of keys with pre-computed placement and cad objects
    """
    result = list()  # type: List[Tuple[int, int, Direction, int, int, Direction]]

    # connections in between neighbours in same row
    # ╭─────╮    ╭─────╮
    # │     │ ←→ │     │
    # ╰─────╯    ╰─────╯
    row_idx = 0
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, len(key_matrix[row_idx]) - 1))
    row_idx = 1
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, len(key_matrix[row_idx]) - 1))
    row_idx = 2
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, 14))
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(15, len(key_matrix[row_idx]) - 1))
    row_idx = 3
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, 14))
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(15, len(key_matrix[row_idx])-1))
    row_idx = 4
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, len(key_matrix[row_idx])))
    row_idx = 5
    result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT) for k in range(1, len(key_matrix[row_idx])))

    # connections in between keys in adjacent rows
    #            ╭───────╮    ╭──────╮   ╭─────╮   ╭─────╮   ╭─────╮    ╭───────────╮
    #            │       │    │      │   │     │   │     │   │     │    │           │
    #            ╰───────╯    ╰──────╯   ╰─────╯   ╰─────╯   ╰─────╯    ╰───────────╯
    #                ↕          ↕                                              ↕
    #            ╭─────╮   ╭─────╮   ╭───────────────────────╮   ╭─────╮   ╭──────╮
    #            │     │   │     │   │                       │   │     │   │      │
    #            ╰─────╯   ╰─────╯   ╰───────────────────────╯   ╰─────╯   ╰──────╯



    return result


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_connector_face_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, Direction, Direction, int, int, Direction, Direction, Direction]]:
    """
    Specifies which key-connectors' face are to be connected.
    @param key_matrix: pool of keys with pre-computed placement and cad objects

     ╭─────╮   ╭─────╮
     │     │   │     │
     ╰─────╯   ╰─────╯
             ↕
     ╭─────╮   ╭─────╮
     │     │   │     │
     ╰─────╯   ╰─────╯
    """
    result = list()  # type: List[Tuple[int, int, Direction,  Direction, Direction, int, int, Direction,  Direction, Direction,]]
    return result


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_key_corner_edge_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, List[Tuple[cadquery.Vector, cadquery.Vector]], Direction]]:
    """
    Example of one horizontal gap filler in between two rows with keys having different column span.
              ╭───────╮    ╭──────╮   ╭─────╮   ╭─────╮   ╭─────╮    ╭───────────╮
              │       │    │      │   │     │   │     │   │     │    │           │
    edge  0  ↗╰───────╯↖  ↗╰──────╯↖ ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖  ↗╰───────────╯↖ edge 11
    edge 21  ↘╭─────╮↙ ↘╭─────╮↙ ↘╭───────────────────────╮↙ ↘╭─────╮↙ ↘╭──────╮↙ edge 12
              │     │   │     │   │                       │   │     │   │      │
              ╰─────╯   ╰─────╯   ╰───────────────────────╯   ╰─────╯   ╰──────╯
    """
    result = list()  # type: List[Tuple[int, int, List[Tuple[cadquery.Vector, cadquery.Vector]], Direction]]

    # row 0 to 1

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 0
    for key_idx in range(0, len(key_matrix[row_idx])):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 1
    for key_idx in range(len(key_matrix[row_idx]) - 1, 0, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 0, loft, Direction.FRONT))

    # row 1 to 2

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 1
    for key_idx in range(0, len(key_matrix[row_idx])):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 2
    for key_idx in range(len(key_matrix[row_idx]), 0, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible or True:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 0, loft, Direction.FRONT))

    # row 2 to 3

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 2
    for key_idx in range(0, 13):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 3
    for key_idx in range(13, 0, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 0, loft, Direction.FRONT))

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 2
    for key_idx in range(14, 20):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 3
    for key_idx in range(20, 14, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 14, loft, Direction.FRONT))

    # row 3 to 4

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 3
    for key_idx in range(0, len(key_matrix[row_idx])):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 4
    for key_idx in range(len(key_matrix[row_idx]), 0, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 0, loft, Direction.FRONT))

    # row 4 to 5

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    row_idx = 4
    for key_idx in range(0, len(key_matrix[row_idx])):
        key = key_matrix[row_idx][key_idx]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    row_idx = 5
    for key_idx in range(len(key_matrix[row_idx]), 0, -1):
        key = key_matrix[row_idx][key_idx - 1]
        if key.base.is_visible:
            loft.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
            loft.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((row_idx, 0, loft, Direction.FRONT))

    # manually connect leftovers

    # iso enter - center-left wedge

    def get_cad_corner_center_edge(cad_object: cadquery.Workplane, key_base: KeyBase, inner: bool = True) -> Tuple[cadquery.Vector, cadquery.Vector]:
        face = cad_object.faces("|Y").faces("<X")
        point = key_base.position if inner else (key_base.position[0] - key_base.width, key_base.position[1], key_base.position[2])
        edge = face.edges("|Z").edges(NearestToPointSelector(point))

        bottom = edge.vertices("<Z").val().Center()  # type: cadquery.Vertex
        top = edge.vertices(">Z").val().Center()  # type: cadquery.Vertex
        return bottom, top

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    enter_key = key_matrix[3][13]
    left_key = key_matrix[3][12]
    bottom_left_key = key_matrix[2][12]

    loft.append(get_cad_corner_center_edge(enter_key.slot.get_cad_object(), key_base=enter_key.base, inner=False))
    loft.append(get_cad_corner_center_edge(enter_key.slot.get_cad_object(), key_base=enter_key.base, inner=True))

    e = bottom_left_key.connectors.right.get_cad_face(Direction.BACK).edges("|Z").edges(">X")
    loft.append((e.vertices("<Z").val().Center(), e.vertices(">Z").val().Center()))

    loft.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    loft.append(left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

    result.append((3, 12, loft, Direction.FRONT))

    # iso enter - right connector

    top_right_key = key_matrix[3][14]
    bottom_right_key = key_matrix[2][14]

    loft = list()

    loft.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
    loft.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))

    loft.append(top_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
    loft.append(top_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    loft.append(bottom_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
    loft.append(bottom_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))

    result.append((3, 13, loft, Direction.RIGHT))

    # numpad +

    numpad_plus_key = key_matrix[3][len(key_matrix[3]) - 1]
    top_left_key = key_matrix[3][len(key_matrix[3]) - 2]
    bottom_left_key = key_matrix[2][len(key_matrix[2]) - 2]

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    loft.append(top_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    loft.append(top_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

    loft.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    loft.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

    loft.append(numpad_plus_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
    loft.append(numpad_plus_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))

    result.append((3, len(key_matrix[3]) - 2, loft, Direction.RIGHT))

    # numpad enter

    numpad_enter_key = key_matrix[1][len(key_matrix[1]) - 1]
    top_left_key = key_matrix[1][len(key_matrix[1]) - 2]
    bottom_left_key = key_matrix[0][len(key_matrix[0]) - 2]

    loft = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

    loft.append(top_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    loft.append(top_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

    loft.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    loft.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

    loft.append(numpad_enter_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
    loft.append(numpad_enter_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))

    result.append((1, len(key_matrix[1]) - 2, loft, Direction.RIGHT))

    return result
