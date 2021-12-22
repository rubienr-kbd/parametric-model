import cadquery

from key import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyUtils(object):

    @staticmethod
    def set_position_relative_to(key: KeyBase, ref_key: KeyBase, pos: Direction) -> None:
        """
        Defines the key position as top/bottom left/right of the reference key.
        """
        position = None  # type: Optional[Tuple[float,float,float]]
        if pos == Direction.TOP:
            position = (
                ref_key.position[0],
                ref_key.position[1] + ref_key.depth / 2 + ref_key.clearance_top + key.clearance_bottom + key.depth / 2,
                key.position[2])

        elif pos == Direction.BOTTOM:
            position = (
                ref_key.position[0],
                ref_key.position[1] - ref_key.depth / 2 - ref_key.clearance_bottom - key.clearance_top - key.depth / 2,
                key.position[2])

        elif pos == Direction.RIGHT:
            position = (
                ref_key.position[0] + ref_key.width / 2 + ref_key.clearance_right + key.clearance_left + key.width / 2,
                ref_key.position[1],
                key.position[2])

        elif pos == Direction.LEFT:
            position = (
                ref_key.position[0] - ref_key.width / 2 - ref_key.clearance_left - key.clearance_right - key.width / 2,
                ref_key.position[1],
                key.position[2])

        else:
            assert False

        key.position = position

    @staticmethod
    def connector(first_face: cadquery.Workplane, second_face: cadquery.Workplane) -> cadquery.Workplane:

        def get_wire(face):
            return face.first().wires().val()

        return cadquery.Workplane(cadquery.Solid.makeLoft([get_wire(first_face), get_wire(second_face)]))

    @staticmethod
    def key_connector(first_key: Key,
                      second_key: Key,
                      first_direction: Direction,
                      second_direction: Direction) -> cadquery.Workplane:
        """
        Returns a loft/gap filler in between first and second key. The respective faces are specified by the direction.
        @param first_key: the key to loft from
        @param second_key: the key to loft to
        @param first_direction: the face to loft from
        @param second_direction: the face to loft to
        """

        def get_wire(face):
            return face.first().wires().val()

        first_wire = get_wire(first_key.slot.get_cad_face(first_direction))
        second_wire = get_wire(second_key.slot.get_cad_face(second_direction))
        return cadquery.Workplane(cadquery.Solid.makeLoft([first_wire, second_wire]))

    @staticmethod
    def connect_keys(connection_info: List[Tuple[int, int, Direction, int, int, Direction]],
                     key_matrix: List[List[Key]]) -> List[Tuple[Key, Key, cadquery.Workplane]]:
        """
        Creates solids for gaps in between the keys as listed in the connection info.
        @param connection_info: information which keys to connect and which faces to use
        @param key_matrix: pool of keys with pre-computed placement and cad objects
        """
        print("compute key to key connectors ({}) ...".format(len(connection_info)))
        connectors = list()  # type: List[Tuple[Key, Key, cadquery.Workplane]]
        for a_row, a_idx, a_direction, b_row, b_col, b_direction in connection_info:
            print(".", end="")
            a = key_matrix[a_row][a_idx]
            b = key_matrix[b_row][b_col]
            loft = KeyUtils.key_connector(a, b, a_direction, b_direction)
            a.connectors.get_connector(a_direction)._cad_object = loft
            b.connectors.get_connector(b_direction)._cad_object = loft
            connectors.append((a, b, loft))
        print("\ncompute key to key connectors:done")
        return connectors

    @staticmethod
    def connect_connectors(connection_info: List[Tuple[int, int, Direction, Direction, int, int, Direction, Direction]],
                           key_matrix: List[List[Key]]) -> List[Tuple[Key, Key, cadquery.Workplane]]:
        print("compute connector gap filler ({}) ...".format(len(connection_info)))
        connectors = list()  # type: List[Tuple[Key, Key, cadquery.Workplane]]
        for a_row, a_idx, a_direction_x, a_direction_y, b_row, b_col, b_direction_x, b_direction_y in connection_info:
            print(".", end="")
            a = key_matrix[a_row][a_idx]
            b = key_matrix[b_row][b_col]

            if a.connectors.get_connector(Direction.RIGHT).has_cad_object() and b.connectors.get_connector(Direction.RIGHT).has_cad_object():
                a_connector = a.connectors.get_connector(a_direction_x)
                b_connector = b.connectors.get_connector(b_direction_x)
                loft = KeyUtils.connector(
                    a_connector.get_cad_face(a_direction_y),
                    b_connector.get_cad_face(b_direction_y))
                connectors.append((a, b, loft))
        print("\ncompute connector gap filler: done")
        return connectors
