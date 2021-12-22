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
                     key_matrix: List[List[Key]]) -> None:
        """
        Creates solids for gaps in between the keys as listed in the connection info.
        @param connection_info: information which keys to connect and which faces to use
        @param key_matrix: pool of keys with pre-computed placement and cad objects
        """
        print("compute key to key connectors ({}) ...".format(len(connection_info)))

        for a_row, a_idx, a_direction_x, b_row, b_col, b_direction_x in connection_info:
            a = key_matrix[a_row][a_idx]
            b = key_matrix[b_row][b_col]
            if a.slot.has_cad_object() and b.slot.has_cad_object():
                print(".", end="")
                loft = KeyUtils.key_connector(a, b, a_direction_x, b_direction_x)
                a.connectors.get_connector(a_direction_x)._cad_object = loft
                b.connectors.get_connector(b_direction_x)._cad_object = loft

                a.expose_cad_objects()
                b.expose_cad_objects()
            else:
                print("x", end="")
        print("\ncompute key to key connectors: done")

    @staticmethod
    def connect_connectors(connection_info: List[Tuple[int, int, Direction, Direction, int, int, Direction, Direction]],
                           key_matrix: List[List[Key]]) -> None:
        print("compute connector gap filler ({}) ...".format(len(connection_info)))
        for a_row, a_idx, a_direction_x, a_direction_y, b_row, b_col, b_direction_x, b_direction_y in connection_info:
            a = key_matrix[a_row][a_idx]
            b = key_matrix[b_row][b_col]

            a_connector = a.connectors.get_connector(a_direction_x)
            b_connector = b.connectors.get_connector(b_direction_x)
            if a_connector.has_cad_object() and b_connector.has_cad_object():
                print(".", end="")
                a_connector = a.connectors.get_connector(a_direction_x)
                b_connector = b.connectors.get_connector(b_direction_x)
                loft = KeyUtils.connector(
                    a_connector.get_cad_face(a_direction_y),
                    b_connector.get_cad_face(b_direction_y))
                a.connectors.get_connector(a_direction_y)._cad_object = loft
                b.connectors.get_connector(b_direction_y)._cad_object = loft

                a.expose_cad_objects()
                b.expose_cad_objects()
            else:
                print("x", end="")
        print("\ncompute connector gap filler: done")

    @staticmethod
    def remove_cad_objects(key_matrix: List[List[Key]]) -> None:
        """
        Filters out cad objects from view that must be computed due to dependencies.
        @param key_matrix: pool of keys with pre-computed placement and cad objects
        """
        print("removing cad objects ...")
        for row in key_matrix:
            for key in row:
                print("{:7}: ".format(key.name), end="")
                if not GlobalConfig.debug.show_placement:
                    key.cad_objects.plane = None
                    print("plcement", end=" ")
                if not GlobalConfig.debug.render_key_cap:
                    key.cad_objects.cap = None
                    print("cap", end=" ")
                if not GlobalConfig.debug.render_slots:
                    key.cad_objects.slot = None
                    print("slot", end=" ")
                if not GlobalConfig.debug.render_key_switch:
                    key.cad_objects.switch = None
                    print("switch", end=" ")
                if not GlobalConfig.debug.render_connectors:
                    key.cad_objects.connectors = []
                    print("connectors", end=" ")
                print("")
        print("removing cad objects: done")

    @staticmethod
    def squash(key_matrix: List[List[Key]], do_unify: bool, do_clean_union: bool) -> Union[cadquery.Workplane, cadquery.Assembly]:
        """

        @param key_matrix: pool of keys with pre-computed placement and cad objects
        @param do_unify: recommended True for export, False for cadquery editor (cq-editor)
        @param do_clean_union: recommended False for unified export to step file
        @return cadquery.Workplane if unify requested, of cadquery.Assembly otherwise
        """
        print("final assembly ...")
        assembly = cadquery.Assembly()
        union = None  # type: Optional[cadquery.Workplane]

        for row in key_matrix:
            for key in row:
                color = cadquery.Color(0, 0, 1, 0.5) if key.base.is_visible else cadquery.Color(1, 1, 1, 0.125)
                print("{:7}:".format(key.name), end=" ")
                if not key.base.is_visible and not GlobalConfig.debug.show_invisibles:
                    continue

                # key components
                for object_name, cad_object in [(attr_name, value) for attr_name, value in key.cad_objects]:
                    if type(cad_object) is list:
                        continue
                    print("{}".format(object_name))
                    if do_unify:
                        union = cad_object if union is None else union.union(cad_object, clean=do_clean_union)
                    else:
                        assembly = assembly.add(cad_object, color=color)

                # connectors
                for connector in key.cad_objects.connectors:
                    print("{connectors}")
                    if do_unify:
                        union = connector if union is None else union.union(connector, clean=do_clean_union)
                    else:
                        assembly = assembly.add(connector, color=color)


        print("final assembly: done")
        return union if do_unify else assembly
