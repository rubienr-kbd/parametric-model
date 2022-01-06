import operator

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


def apply_translation_offset(key_matrix: List[List[Key]]) -> None:
    """
    Compute extra position offset for non-planar keyboards.
    The extra offset is typically a small offset w.r.t. the real iso layout and applies mostly to Z-axis.
    """

    row_idx = 0
    key_idx = 0
    for row in key_matrix:
        for key in row:
            if row_idx == 0 and key_idx == 3:
                key.base.position_offset = tuple(map(operator.add, key.base.position_offset, (0, 0, 2)))
            if row_idx == 1 and key_idx == 1:
                key.base.position_offset = tuple(map(operator.add, key.base.position_offset, (0, 0, 2)))
            else:
                key.base.position_offset = tuple(map(operator.add, key.base.position_offset, (0, 0, 0)))
            key_idx += 1
        key_idx = 0
        row_idx += 1


def compute_placement_and_cad_objects(key_matrix: List[List[Key]]) -> None:
    print("compute key placement and cad objects ...")
    last_row = None
    last_key = None
    row_idx = 0
    for row in key_matrix:
        print("row {}".format(row_idx))
        print("  col│position x   position y   position z  │rotation x   rotation y   rotation z  |key   unit│clrto clrri clrbo clrle│capwi  capde capth│vis")
        print("  ───┼──────────────────────────────────────┼──────────────────────────────────────┼──────────┼───────────────────────┼──────────────────┼───")
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

            print("  {col:2} "
                  "│{x:6.2f}{x_off:+6.2f} {y:6.2f}{y_off:+6.2f} {z:6.2f}{z_off:+6.2f}"
                  "|{rot_x:6.2f}{rot_x_off:+6.2f} {rot_y:6.2f}{rot_y_off:+6.2f} {rot_z:6.2f}{rot_z_off:+6.2f}"
                  "│{key:5} {unit:4.2f}"
                  "│{clrto:5.2f} {clrri:5.2f} {clrbo:5.2f} {clrle:5.2f}"
                  "│{capwi:6.2f} {capde:5.2f} {capth:5.2f}"
                  "│{vis}"
                  .format(col=col_idx,
                          x=key.base.position[0], y=key.base.position[1], z=key.base.position[2],
                          x_off=key.base.position_offset[0], y_off=key.base.position_offset[1], z_off=key.base.position_offset[2],
                          rot_x=key.base.rotation[0], rot_y=key.base.rotation[1], rot_z=key.base.rotation[2],
                          rot_x_off=key.base.rotation_offset[0], rot_y_off=key.base.rotation_offset[1], rot_z_off=key.base.rotation_offset[2],
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

"""
    Gap filling terms:
    
    a ... horizontal filler
    b ... vertical filler
    c ... intersection filler
    
     ╭─────╮ ← → ╭─────╮
     │     │  a  │     │
     ╰─────╯↖   ↗╰─────╯
       ↕ b    c    b ↕
     ╭─────╮↙   ↘╭─────╮
     │     │  a  │     │
     ╰─────╯ ← → ╰─────╯
     
     Notes: 
       If all keys are planar (share the same surface) then loft can be used as filler.
       If keys have rotations and displacement w.r.t. to the planar distribution polyhedron shall be used as filler.
"""


def get_key_face_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, int, int, Direction, bool]]:
    """
    Specifies which keys and which keys' face are to be connected.
    @param key_matrix: pool of keys with pre-computed placement and cad objects
    """
    result = list()  # type: List[Tuple[int, int, Direction, int, int, Direction, bool]]

    polyhedron_mode = True

    def horizontal_face_gap_filler():
        """
        connections in between neighbours in same row
        ╭─────╮    ╭─────╮
        │     │ ←→ │     │
        ╰─────╯    ╰─────╯
        """
        row_idx = 0
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, len(key_matrix[row_idx]) - 1))
        row_idx = 1
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, len(key_matrix[row_idx]) - 1))
        row_idx = 2
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, 14))
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(15, len(key_matrix[row_idx]) - 1))
        row_idx = 3
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, 14))
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(15, len(key_matrix[row_idx]) - 1))
        row_idx = 4
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, len(key_matrix[row_idx])))
        row_idx = 5
        result.extend((row_idx, k - 1, Direction.RIGHT, row_idx, k, Direction.LEFT, polyhedron_mode) for k in range(1, len(key_matrix[row_idx])))

    horizontal_face_gap_filler()

    def vertical_face_gap_filler():
        """
        connections in between keys in adjacent rows
        ╭───────╮    ╭──────╮   ╭─────╮   ╭─────╮   ╭─────╮    ╭───────────╮
        │       │    │      │   │     │   │     │   │     │    │           │
        ╰───────╯    ╰──────╯   ╰─────╯   ╰─────╯   ╰─────╯    ╰───────────╯
           ↑             ↗                              ↖            ↑
           ↓          ↙                                    ↘         ↓
        ╭─────╮   ╭─────╮   ╭───────────────────────╮   ╭─────╮   ╭──────╮
        │     │   │     │   │                       │   │     │   │      │
        ╰─────╯   ╰─────╯   ╰───────────────────────╯   ╰─────╯   ╰──────╯
        """

        # connections in between adjacent rows 0 to 1
        row_idx = 0
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(0, 3)))  # LCTL to LALT
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k + 6, Direction.FRONT, polyhedron_mode) for k in range(4, 7)))  # LALT to MENU
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k + 5, Direction.FRONT, polyhedron_mode) for k in range(8, 12)))  # LARR to numpad INS
        result.extend([(row_idx, 12, Direction.BACK, row_idx + 1, 12 + 6, Direction.FRONT, polyhedron_mode)])  # numpad DEL

        # connections in between adjacent rows 1 to 2
        row_idx = 1
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(0, 13)))  # LSFT to RSFT
        result.extend(((row_idx, k - 1, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(14, len(key_matrix[row_idx]))))  # LARR spacer to numpad

        # connections in between adjacent rows 2 to 3
        row_idx = 2
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(0, 13)))  # CSFT to #
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(14, len(key_matrix[row_idx]) - 1)))  # spacer to numpad

        # connections in between adjacent rows 3 to 4
        row_idx = 3
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(0, len(key_matrix[row_idx]))))  # TAB to numpad

        # connections in between adjacent rows 4 to 5
        row_idx = 4
        result.extend(((row_idx, k, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(0, 2)))  # ESC to F4
        result.extend(((row_idx, k + 1, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(2, 9)))  # F5 to F8
        result.extend(((row_idx, k + 2, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(9, 12)))  # F9 to F11
        result.extend(((row_idx, k + 1, Direction.BACK, row_idx + 1, k, Direction.FRONT, polyhedron_mode) for k in range(13, 20)))  # PRNT to numpad -

    vertical_face_gap_filler()

    return result


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# def get_connector_face_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, Direction, Direction, Direction, int, int, Direction, Direction, Direction]]:
#    """
#    Specifies which key-connectors' face are to be connected.
#    @param key_matrix: pool of keys with pre-computed placement and cad objects
#
#     ╭─────╮   ╭─────╮
#     │     │   │     │
#     ╰─────╯   ╰─────╯
#             ↕
#     ╭─────╮   ╭─────╮
#     │     │   │     │
#     ╰─────╯   ╰─────╯
#     TODO: connector faces wich are parallel to Y cannot be selected by |Y if translated in Z direction (assume bug).
#        Do not use this method for not-planar keyboards.
#    """
#    result = list()  # type: List[Tuple[int, int, Direction,  Direction, Direction, int, int, Direction,  Direction, Direction,]]
#    return result
#    # rows 0 to 1
#    result.extend(((0, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 1, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(0, 3)))  # LCTL to LALT
#    result.extend(((0, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 1, k + 6, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(3, 6)))  # RALT to FN
#    result.extend(((0, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 1, k + 5, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(7, 11)))  # RCTL to numpad NINS
#    result.extend(((0, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 1, k + 6, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(11, 13)))  # numpad NDEL
#
#    # rows 1 to 2
#    result.extend(((1, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 2, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(0, 12)))  # LSFT to RSFT
#    result.extend(((1, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 2, k + 1, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in
#                   range(13, len(key_matrix[2]) - 1)))  # spacer to numpad
#
#    # rows 2 to 3
#    result.extend(((2, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 3, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(0, 12)))  # CSFT to #
#    result.extend(
#        ((2, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 3, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(13, len(key_matrix[2]) - 1)))  # spacer to numpad
#
#    # rows 3 to 4
#    result.extend(
#        ((3, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 4, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(0, len(key_matrix[3]) - 1)))  # TAB to numpad
#
#    # rows 4 to 5
#    result.extend(((4, k, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 5, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(0, 4)))  # ESC to F4
#    result.extend(((4, k + 1, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 5, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(4, 8)))  # F5 to F7
#    result.extend(((4, k + 2, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 5, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(8, 11)))  # F18 to F10
#    result.extend(((4, k + 1, Direction.RIGHT, Direction.BACK, Direction.BACK_RIGHT, 5, k, Direction.RIGHT, Direction.FRONT, Direction.FRONT_RIGHT) for k in range(13, 19)))  # F18 to F10

#    return result


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _get_key_intersection_gap_filler_edges(key_matrix: List[List[Key]], bottom_left_row_idx: int, bottom_left_key_idx: int, top_left_key_idx: int) -> List[Tuple[cadquery.Vector, cadquery.Vector]]:
    """
        top left key index
        ↓
     ╭─────╮   ╭─────╮
     │     │   │     │
     ╰─────╯↖ ↗╰─────╯
     ╭─────╮↙ ↘╭─────╮
     │     │   │     │
     ╰─────╯   ╰─────╯
        ↑
        bottom left key index
    """
    result = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
    result.append(key_matrix[bottom_left_row_idx][bottom_left_key_idx].slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
    result.append(key_matrix[bottom_left_row_idx][bottom_left_key_idx + 1].slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
    result.append(key_matrix[bottom_left_row_idx + 1][top_left_key_idx + 1].slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
    result.append(key_matrix[bottom_left_row_idx + 1][top_left_key_idx].slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
    return result


def get_key_corner_edge_connection_mapping(key_matrix: List[List[Key]]) -> List[Tuple[int, int, List[Tuple[cadquery.Vector, cadquery.Vector]], Direction, bool]]:
    """
    @return a list of tuples containing
        - the key index where to attach the connector,
        - a list of tuples (edges) of two vertex
        - the direction where to attach the key connector
        - a flag indicating polyhedron mode (True) or naive loft mode (False)
    """

    polyhedron_mode = True
    result = list()  # type: List[Tuple[int, int, List[Tuple[cadquery.Vector, cadquery.Vector]], Direction, bool]]

    def intersection_filling():
        """
        intersection filling with polyhedrons
        ╭─────╮   ╭─────╮
        │     │   │     │
        ╰─────╯↖ ↗╰─────╯
        ╭─────╮↙ ↘╭─────╮
        │     │   │     │
        ╰─────╯   ╰─────╯
        """

        # row 0 to 1

        row_idx = 0
        for key_idx in range(0, 3):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(3, 6):
            result.append((row_idx + 1, key_idx + 6, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 6), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(7, 11):
            result.append((row_idx + 1, key_idx + 5, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 5), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(11, 12):
            result.append((row_idx + 1, key_idx + 6, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 6), Direction.FRONT_RIGHT, polyhedron_mode))

        # row 1 to 2

        row_idx = 1
        for key_idx in range(0, 12):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(12, 18):
            result.append((row_idx + 1, key_idx + 1, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 1), Direction.FRONT_RIGHT, polyhedron_mode))

        # row 2 to 3

        row_idx = 2
        for key_idx in range(0, 12):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(14, 19):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))

        # row 3 to 4

        row_idx = 3
        for key_idx in range(0, 20):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))

        # row 4 to 5

        row_idx = 4
        for key_idx in range(0, 1):
            result.append((row_idx + 1, key_idx + 0, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx + 0), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(2, 9):
            result.append((row_idx + 1, key_idx - 1, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx - 1), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(10, 13):
            result.append((row_idx + 1, key_idx - 2, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx - 2), Direction.FRONT_RIGHT, polyhedron_mode))
        for key_idx in range(13, 20):
            result.append((row_idx + 1, key_idx - 1, _get_key_intersection_gap_filler_edges(key_matrix, row_idx, key_idx, key_idx - 1), Direction.FRONT_RIGHT, polyhedron_mode))

    intersection_filling()

    # manually connect leftovers (wedges, triangles, keys with row span > 1 or col span > 1, etc)

    def vertical_spc_gap_filler():
        """
                  ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭─────╮   ╭───────────╮
        row 1     │  0  │   │  1  │   │  2  │   │  3  │   │  4  │   │  5  │   │  6  │   │  7  │   │  8  │   │  9  │   │    10     │
                  ╰─────╯   ╰─────╯   ╰─────╯  ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖ ↗╰─────╯↖  ╰───────────╯
                  ╭────────╮   ╭─────╮   ╭─────╮  ↘╭───────────────────────────────────────────────────────────╮↙  ╭─────╮   ╭──────╮
        row 0     │   0    │   │  1  │   │  2  │   │                           3                               │   │  4  │   │  5   │
                  ╰────────╯   ╰─────╯   ╰─────╯   ╰───────────────────────────────────────────────────────────╯   ╰─────╯   ╰──────╯
        """

        spc_key = key_matrix[0][3]
        b_key = key_matrix[1][6]

        def helper(keys_idx, spc_x_direction):
            """
            Connect one SPC key corner (back left / back right) with all specified keys' front edges except of last key where only the nearest front edge is connected.
            """
            gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
            row_idx = 1
            last_key_idx = keys_idx[-1]

            for key_idx in keys_idx:
                key = key_matrix[row_idx][key_idx]
                if (not key_idx == last_key_idx and spc_x_direction == Direction.RIGHT) or spc_x_direction == Direction.LEFT:
                    gap_filler.append(key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
                if (not key_idx == last_key_idx and spc_x_direction == Direction.LEFT) or spc_x_direction == Direction.RIGHT:
                    gap_filler.append(key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
                gap_filler.append(spc_key.slot.get_cad_corner_edge(spc_x_direction, Direction.BACK))
            return gap_filler

        result.append((0, 3, helper([3, 4, 5, 6], Direction.LEFT), Direction.BACK_LEFT, polyhedron_mode))
        result.append((0, 3, helper([9, 8, 7, 6], Direction.RIGHT), Direction.BACK_RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(b_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(b_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(spc_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(spc_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((0, 3, gap_filler, Direction.BACK, polyhedron_mode))

    vertical_spc_gap_filler()

    def rctl_rsft_triangle():
        # triangle in between RCTL and RSFT
        menu_key = key_matrix[0][6]
        rctl_key = key_matrix[0][7]
        rsft_key = key_matrix[1][12]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(rctl_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(rctl_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(rsft_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        result.append((0, 7, gap_filler, Direction.BACK, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(menu_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(rctl_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(rsft_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        result.append((0, 6, gap_filler, Direction.BACK_RIGHT, polyhedron_mode))

    rctl_rsft_triangle()

    def numpad_mins_triangle():
        # triangle in between numpad 1, numpad 2 and NINS

        np1_key = key_matrix[1][16]
        np2_key = key_matrix[1][17]
        nins_key = key_matrix[0][11]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np1_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(np2_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(nins_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((1, 16, gap_filler, Direction.FRONT_RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np2_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(np2_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(nins_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((1, 17, gap_filler, Direction.FRONT, polyhedron_mode))

    numpad_mins_triangle()

    def frow_numrow_tirangles():
        # triangle in between F1, F2 and 2

        f1_key = key_matrix[5][1]
        num1_key = key_matrix[4][1]
        num2_key = key_matrix[4][2]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(f1_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(num2_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(num2_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((4, 2, gap_filler, Direction.BACK, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(num1_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(num2_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(f1_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        result.append((4, 1, gap_filler, Direction.BACK_RIGHT, polyhedron_mode))

        # triangle in between F8, F9 and 0

        f8_key = key_matrix[5][8]
        num9_key = key_matrix[4][9]
        num0_key = key_matrix[4][10]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(f8_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(num0_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(num0_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((4, 10, gap_filler, Direction.BACK, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(num9_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(num0_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(f8_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        result.append((4, 9, gap_filler, Direction.BACK_RIGHT, polyhedron_mode))

        # triangle in between F11, F12 and BSP

        f11_key = key_matrix[5][11]
        f12_key = key_matrix[5][12]
        bsp_key = key_matrix[4][13]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(f12_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(f12_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(bsp_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((5, 12, gap_filler, Direction.FRONT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(f11_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(f12_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(bsp_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((5, 11, gap_filler, Direction.FRONT_RIGHT, polyhedron_mode))

    frow_numrow_tirangles()

    def iso_enter_filling():
        # iso enter

        # center-left wedge

        def get_cad_corner_center_edge(cad_object: cadquery.Workplane, key_base: KeyBase, inner: bool = True) -> Tuple[cadquery.Vector, cadquery.Vector]:
            face = cad_object.faces("|Y").faces("<X")
            point = key_base.position if inner else (key_base.position[0] - key_base.width, key_base.position[1], key_base.position[2])
            edge = face.edges("|Z").edges(NearestToPointSelector(point))

            bottom = edge.vertices("<Z").val().Center()  # type: cadquery.Vertex
            top = edge.vertices(">Z").val().Center()  # type: cadquery.Vertex
            return bottom, top

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]

        enter_key = key_matrix[3][13]
        left_key = key_matrix[3][12]
        bottom_left_key = key_matrix[2][12]

        gap_filler.append(get_cad_corner_center_edge(enter_key.slot.get_cad_object(), key_base=enter_key.base, inner=False))
        gap_filler.append(get_cad_corner_center_edge(enter_key.slot.get_cad_object(), key_base=enter_key.base, inner=True))

        e = bottom_left_key.connectors.right.get_cad_face(Direction.BACK).edges("|Z").edges(">X")
        gap_filler.append((e.vertices("<Z").val().Center(), e.vertices(">Z").val().Center()))

        gap_filler.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))

        result.append((3, 12, gap_filler, Direction.FRONT_RIGHT, polyhedron_mode))

        # bottom triangle
        bottom_key = key_matrix[1][12]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(bottom_left_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(bottom_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((3, 13, gap_filler, Direction.FRONT_LEFT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(bottom_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((3, 13, gap_filler, Direction.FRONT, polyhedron_mode))

        # right connector
        top_right_key = key_matrix[3][14]
        bottom_right_key = key_matrix[2][14]
        bottom_key_right_spacer = key_matrix[1][13]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(top_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(top_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(bottom_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(bottom_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        result.append((3, 13, gap_filler, Direction.RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(enter_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(bottom_right_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(bottom_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(bottom_key_right_spacer.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((3, 13, gap_filler, Direction.FRONT_RIGHT, polyhedron_mode))

    iso_enter_filling()

    def nent_ndel_connectors():
        # horizontal gap in between numpad 3, NDEL and NENT

        ndel_key = key_matrix[0][len(key_matrix[0]) - 2]
        np3_key = key_matrix[1][len(key_matrix[1]) - 2]
        nent_key = key_matrix[1][len(key_matrix[1]) - 1]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np3_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(np3_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((1, len(key_matrix[1]) - 2, gap_filler, Direction.RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np3_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(ndel_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((0, len(key_matrix[0]) - 2, gap_filler, Direction.BACK_RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(ndel_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(ndel_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((0, len(key_matrix[0]) - 2, gap_filler, Direction.RIGHT, polyhedron_mode))

        # horizontal gap in between numpad 9, numpad 6 and NPLU

        np9_key = key_matrix[3][len(key_matrix[3]) - 2]
        nplu_key = key_matrix[3][len(key_matrix[3]) - 1]
        np6_key = key_matrix[2][len(key_matrix[2]) - 2]

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np9_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(np9_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((3, len(key_matrix[3]) - 2, gap_filler, Direction.RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np9_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(np6_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((2, len(key_matrix[2]) - 2, gap_filler, Direction.BACK_RIGHT, polyhedron_mode))

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(np6_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(np6_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        result.append((2, len(key_matrix[2]) - 2, gap_filler, Direction.RIGHT, polyhedron_mode))

        # intersection in between numpad 6, numpad 3, NPLU and NENT

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(np6_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(np3_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        result.append((2, len(key_matrix[2]) - 2, gap_filler, Direction.FRONT_RIGHT, polyhedron_mode))

        # vertical gap in between NPLU and NENT

        gap_filler = list()  # type: List[Tuple[cadquery.Vector, cadquery.Vector]]
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.FRONT))
        gap_filler.append(nplu_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.FRONT))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.RIGHT, Direction.BACK))
        gap_filler.append(nent_key.slot.get_cad_corner_edge(Direction.LEFT, Direction.BACK))
        result.append((3, len(key_matrix[3]) - 1, gap_filler, Direction.FRONT, polyhedron_mode))

    nent_ndel_connectors()

    return result
