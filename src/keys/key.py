from typing import Optional, Dict
import math
from .key_mixins import *
from src import model_importer
_cliargs, config = model_importer.import_config()


"""
Indexing and terms:

             first key (keys are not aligned to columns)
             ↓
         ╭─────────────────────────────────────────────────────────────────────────────────────╮
row 5 →  │  ESC F1  F2  F3  F4  F5  F6  F7  F8  F9 F10 F11 F12  PR  SL  PA        .   .   .    │
         │   ^   1   2   3   4   5   6   7   8   9   0  ... ←   INS P1  PUP    NUM  /   *   -  │
         │   ⇄   q w e r ...                                ↲   DEL END PDN     7   8   9   +  │
         │   ⇓   a s d f ...                                ↲                   4   5   6   +  │
         │   ⇑   < y x c ...                                ⇑         ↑         1   2   3  ENT │
row 0 →  │  LCTL ... LALT           SPACE        RALT ... RCTL    ←   ↓   →    INS INS DEL ENT │
         ╰─────────────────────────────────────────────────────────────────────────────────────╯

- row left/right direction may be aso denoted as x, x-direciton or x-axis
- row up/down direction may also be denoted as y, y-direction or y-axis

- key/switch
  - width            ... x-axis
  - depth            ... y-axis
  - height/thickness ... z-axis

Construction strategy:
  Placement:
    1. Each key has as a base the key_base-plane. The rectangular plane is centered at position 0/0/0 parallel to XY.
    2. The first key (bottom/left) placed, then its right neighbours.
    3. Each subsequent neighbor plane is placed relative to its left neighbour.
    4. Each first key of subsequent rows is placed relatively to its lower neighbour, etc.
  Construction:
    Each key related component (key-cap, switch, switch slot, debug items, etc.) is constructed relatively to the base plane.
    Technically the components undergo the same translation than the base plane.
    The Key object implements the key related components (key-cap, switch, switch slot, debug items) as members.
    The aim is to firstly calculate a simple model in python, and then compute all 3D-objects for cadquery.
    For this reason the components expose methods for
      - resolving/computing the input parameters: update()
      - computing the cad object according to the input parameters: compute()
      - retrieving the computed cad object: get_cad_object()


  Illustration of base plane, key and origin:

    ⊙ ... origin
    * ... switch
    ⨯ ... stabilizer
    ⊛ ... origin + switch
    ⨂ ... origin + stabilizer

         ↓ 1 unit base plane: usually 19mm x 19mm
    ╔═════════╗  ╭─────╮
    ║         ║  │     │ ← 1 unit key: slightly smaller, usually 18mm x 18mm
    ║    ⊙    ║  ╰─────╯
    ║         ║
    ╚═════════╝
                                    ↓ 2 unit width                              iso enter ↓           ↓ numpad enter or +
                  ╔═════════╗╔═════════════╗╔══════════════════════════════════════╗╔═══════════╗╔═════════╗
                  ║ ╭─────╮ ║║ ╭─────────╮ ║║  ╭─────────────────────────────────╮ ║║ ╭───────╮ ║║ ╭─────╮ ║
  1 unit height → ║ │  ⊛  │ ║║ │    ⊛    │ ║║  │   ⨯           ⊛            ⨯    │ ║║ │   ⨯   │ ║║ │  ⨯  │ ║
                  ║ ╰─────╯ ║║ ╰─────────╯ ║║  ╰─────────────────────────────────╯ ║║ ╰╮      │ ║║ │     │ ║ ← 2 unit height
                  ╚═════════╝╚═════════════╝╚══════════════════════════════════════╝║  │  ⊛   │ ║║ │  ⊛  │ ║
                      ↑ 1 unit width                           ↑ space              ║  │      │ ║║ │     │ ║
                                                                                    ║  │  ⨯   │ ║║ │  ⨯  │ ║
                                                                                    ║  ╰──────╯ ║║ ╰─────╯ ║
                                                                                    ╚═══════════╝╚═════════╝
"""


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ObjectCache(object):

    def __init__(self, config: DEBUG):
        self.container = dict()  # type: Dict[str, cadquery.Workplane]
        self.enabled = not config.disable_object_cache

    @staticmethod
    def cache_name(attr_1: str, *args: str) -> str:
        attrs = "-".join(["({})".format(arg) for arg in args])
        return "({}){}{}".format(attr_1, "-" if len(attrs) > 0 else "", attrs)

    def store(self, obj: cadquery.Workplane, attr_1: str, *args: str) -> None:
        if not self.enabled:
            return
        key = ObjectCache.cache_name(attr_1, *args)

        if key in self.container:
            print("failed to cache object with id {}".format(key))
            assert False
        self.container[key] = obj

    def get(self, attr_1: str, *args: str) -> Optional[cadquery.Workplane]:
        if not self.enabled:
            return None
        else:
            key = ObjectCache.cache_name(attr_1, *args)
            return self.container[key] if key in self.container else None


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyBase(KeyPlane, Computeable, CadObject, KeyBaseMixin):
    def __init__(self, config: config.KeyBaseConfig) -> None:
        super(KeyBase, self).__init__()
        self.unit_length = config.unit_length  # type: float
        self.unit_width_factor = 1  # type: float
        self.unit_depth_factor = 1  # type: float
        self.clearance_left = config.clearance_x  # type: float
        self.clearance_right = config.clearance_x  # type: float
        self.clearance_top = config.clearance_y  # type: float
        self.clearance_bottom = config.clearance_y  # type: float
        # placeholder key slot may be:
        #  - visible or invisible, e.g. normal key vs invisible placeholder near arrow up
        #  - connected or disconnected, e.g. placeholder below iso-enter vs placeholder near arrow up
        #  - unfilled or filled, e.g. placeholder near arrow up vs placeholder below numpad enter
        self.is_visible = True  # type: bool
        self.is_filled = False  # type: bool
        self.is_connected_left = True  # type: bool
        self.is_connected_right = True  # type: bool
        self.is_connected_front = True  # type: bool
        self.is_connected_back = True  # type: bool

    @property
    def is_connected(self) -> bool:
        return self.is_connected_left and self.is_connected_right and self.is_connected_front and self.is_connected_back

    @is_connected.setter
    def is_connected(self, value: bool):
        self.is_connected_left = value
        self.is_connected_right = value
        self.is_connected_front = value
        self.is_connected_back = value

    def update(self) -> None:
        self.width = self.unit_width_factor * self.unit_length
        self.depth = self.unit_depth_factor * self.unit_length


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KeyCap(KeyBox, Computeable, CadObject):
    def __init__(self, config: config.KeyCapConfig) -> None:
        super(KeyCap, self).__init__()
        self.width_clearance = config.width_clearance  # type: float
        self.depth_clearance = config.depth_clearance  # type: float
        self.thickness = config.thickness  # type: float
        self.z_clearance = config.z_clearance  # type: float
        self.dish_inset = config.dish_inset  # type: float
        self.width = 0  # type: float
        self.depth = 0  # type: float

    def update(self, unit_width_factor: float = 1, unit_depth_factor: float = 1, unit_length: float = config.MODEL_CONFIG.key_base.unit_length, *args, **kwargs) -> None:
        self.width = unit_width_factor * unit_length - self.width_clearance
        self.depth = unit_depth_factor * unit_length - self.depth_clearance

    def compute(self, cache: ObjectCache, *args, **kwargs) -> None:
        cached = cache.get("cap", str(self.width), str(self.depth))
        if cached is None:
            displacement = (0, 0, self.z_clearance)  # type: Tuple[float, float, float]
            self._cad_object = cadquery.Workplane() \
                .wedge(self.width,
                       self.thickness,
                       self.depth,
                       1,
                       1,
                       self.width - 1,
                       self.depth - 1,
                       centered=(True, False, True)) \
                .rotate((0, 0, 0), (1, 0, 0), 90) \
                .translate(displacement)
            cache.store(self._cad_object, "cap", str(self.width), str(self.depth))
        else:
            self._cad_object = cached


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeySwitchSlot(KeyBox, Computeable, CadObject):
    def __init__(self, config: config.KeySwitchSlotConfig) -> None:
        super(KeySwitchSlot, self).__init__()
        self.slot_width = config.width  # type: float
        self.slot_depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float
        self.undercut_depth = config.undercut_depth  # type: float
        self.undercut_width = config.undercut_width  # type: float
        self.undercut_thickness = config.undercut_thickness  # type: float

    def compute(self, basis_face: cadquery.Workplane, do_fill: bool, cache: ObjectCache, *args, **kwargs) -> None:
        """
        To ensure the key cap clearance in cse keys are not placed planar,
        we use the key cap footprint as base size for the key slot.

        @precondition: key cap cad object has been computed
        @param basis_face: the bottom face of the key cap
        @param do_fill: compute skin rather than slot
        @param cache: container for lookup or storing
        """

        # use diagonals as further caching attributes
        tl = basis_face.vertices("<X and >Y").val()  # type: cadquery.Vertex
        tr = basis_face.vertices(">X and >Y").val()  # type: cadquery.Vertex
        # TODO "<X and <Y" sometimes returns a Vector insted of Vertice
        #   bl = basis_face.vertices("<X and <Y").val()  # type: cadquery.Vertex
        bl = basis_face.vertices("<X").val()  # type: cadquery.Vertex
        br = basis_face.vertices(">X and <Y").val()  # type: cadquery.Vertex
        diag1 = math.dist([tl.X, tl.Y], [br.X, br.Y])
        diag2 = math.dist([tr.X, tr.Y], [bl.X, bl.Y])

        cached = cache.get("slot", str(diag1), str(diag2), str(do_fill))

        if cached is None:
            offset = basis_face.vertices(">Z").first().val()  # type: cadquery.Vertex
            z_offset = offset.Z

            if do_fill:
                skin = cadquery.Workplane().sketch() \
                    .face(basis_face.edges().vals()).faces("<Z") \
                    .finalize().extrude(-self.thickness) \
                    .translate((0, 0, -z_offset))
                self._cad_object = skin
            else:
                top = cadquery.Workplane().sketch() \
                    .face(basis_face.edges().vals()).faces("<Z") \
                    .rect(self.slot_width, self.slot_depth, angle=90, mode="s", tag="slot").finalize().extrude(-self.undercut_thickness) \
                    .translate((0, 0, -z_offset))

                undercut_front = cadquery.Workplane() \
                    .box(self.undercut_width, self.undercut_depth, self.thickness) \
                    .translate((0, -self.slot_depth / 2 - self.undercut_depth / 2, -self.undercut_thickness - self.thickness / 2))
                undercut_back = undercut_front.mirror("XZ")
                undercut_left = cadquery.Workplane() \
                    .box(self.undercut_depth, self.undercut_width, self.thickness) \
                    .translate((-self.slot_width / 2 - self.undercut_depth / 2, 0, -self.undercut_thickness - self.thickness / 2))
                undercut_right = undercut_left.mirror("YZ")
                undercut = undercut_front.union(undercut_right).union(undercut_back).union(undercut_left)

                bottom = cadquery.Workplane().sketch().face(top.faces("<Z").edges().vals()).faces("<Z") \
                    .finalize().extrude(-(self.thickness - self.undercut_thickness))
                self._cad_object = top.union(bottom.cut(undercut))

            cache.store(self._cad_object, "slot", str(diag1), str(diag2), str(do_fill))
        else:
            self._cad_object = cache.get("slot", str(diag1), str(diag2), str(do_fill))

    def get_cad_corner_edge(self, direction_x: Direction, direction_y: Direction) -> Tuple[cadquery.Vector, cadquery.Vector]:
        if direction_y is Direction.BACK:
            face = self.get_cad_object().faces(">Y")  # type: Optional[cadquery.Workplane]
        elif direction_y is Direction.FRONT:
            face = self.get_cad_object().faces("<Y")  # type: Optional[cadquery.Workplane]
        else:
            assert False

        if direction_x is Direction.LEFT:
            edge = face.edges("<X")
        elif direction_x is Direction.RIGHT:
            edge = face.edges(">X")
        else:
            assert False

        bottom = edge.vertices("<Z").val().Center()  # type: cadquery.Vertex
        top = edge.vertices(">Z").val().Center()  # type: cadquery.Vertex
        return bottom, top

    def get_cad_corner_vertex(self, direction_x: Direction, direction_y: Direction, direction_z: Direction) -> cadquery.Vector:
        """
        Example:
            e = cadquery.Edge.makeLine(
                o.get_cad_corner_vertex(Direction.LEFT, Direction.BACK, Direction.TOP),
                o.get_cad_corner_vertex(Direction.RIGHT, Direction.BACK, Direction.BOTTOM))

        @param direction_x: left or right
        @param direction_y: front or back
        @param direction_z: top or bottom
        @return:
        """

        if direction_z == Direction.TOP:
            face = self.get_cad_object().faces(">Z")  # type: Optional[cadquery.Workplane]
        elif direction_z == Direction.BOTTOM:
            face = self.get_cad_object().faces("<Z")  # type: Optional[cadquery.Workplane]
        else:
            assert False

        if direction_y is Direction.BACK:
            face = face.vertices(">Y")
        elif direction_y is Direction.FRONT:
            face = face.vertices("<Y")
        else:
            assert False

        if direction_x is Direction.LEFT:
            return face.vertices("<X").val().Center()
        elif direction_x is Direction.RIGHT:
            return face.vertices(">X").val().Center()
        else:
            assert False

    def get_cad_face(self, direction: Direction) -> cadquery.Workplane:
        if direction is Direction.FRONT:
            return self._cad_object.faces("|Y").faces("<Y")
        elif direction is Direction.BACK:
            return self._cad_object.faces("|Y").faces(">Y")
        elif direction is Direction.LEFT:
            return self._cad_object.faces("|X").faces("<X")
        elif direction is Direction.RIGHT:
            return self._cad_object.faces("|X").faces(">X")
        else:
            assert False


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyConnector(CadObject):

    def __init__(self):
        super(KeyConnector, self).__init__()

    def get_cad_face(self, direction: Direction) -> cadquery.Workplane:
        if direction is Direction.FRONT:
            return self._cad_object.faces("|Y").faces("<Y")
        elif direction is Direction.BACK:
            return self._cad_object.faces("|Y").faces(">Y")
        elif direction is Direction.LEFT:
            return self._cad_object.faces("|X").faces("<X")
        elif direction is Direction.RIGHT:
            return self._cad_object.faces("|X").faces(">X")
        else:
            assert False


class KeyConnectors(IterableObject):
    def __init__(self):
        self.front = KeyConnector()
        self.back = KeyConnector()
        self.left = KeyConnector()
        self.right = KeyConnector()
        #self.back_left = KeyConnector()
        #self.back_right = KeyConnector()
        #self.front_left = KeyConnector()
        #self.front_right = KeyConnector()

    def get_connector(self, direction: Direction) -> KeyConnector:
        if direction is Direction.LEFT:
            return self.left
        elif direction is Direction.RIGHT:
            return self.right
        elif direction is Direction.FRONT:
            return self.front
        elif direction is Direction.BACK:
            return self.back
        else:
            assert False


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeySwitch(KeyBox, Computeable, CadObject):

    def __init__(self, config: config.KeySwitchConfig) -> None:
        super(KeySwitch, self).__init__()
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CadObjects(IterableObject):
    def __init__(self):
        self.plane = None  # type: Optional[Shape]
        self.origin = None  # type: Optional[Shape]
        self.name = None  # type: Optional[Shape]
        self.cap = None  # type: Optional[Shape]
        self.slot = None  # type: Optional[Shape]
        self.switch = None  # type: Optional[Shape]
        self.connectors = list()  # type: List[Shape]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Key(Computeable, CadKeyMixin):
    object_cache = ObjectCache(DEBUG)

    def __init__(self) -> None:
        self.base = KeyBase(config.MODEL_CONFIG.key_base)
        self.cap = KeyCap(config.MODEL_CONFIG.cap)
        self.slot = KeySwitchSlot(config.MODEL_CONFIG.switch_slot)
        self.switch = KeySwitch(config.MODEL_CONFIG.switch)
        self.connectors = KeyConnectors()
        self.cad_objects = CadObjects()
        self.name = ""  # type: str

    def update(self):
        # resolve input parameter dependencies
        self.base.update()
        self.cap.update(unit_width_factor=self.base.unit_width_factor,
                        unit_depth_factor=self.base.unit_depth_factor,
                        unit_length=self.base.unit_length)
        self.switch.update()
        self.slot.update()

    def compute(self):
        # compute key components at coordinate origin
        self.base.compute()
        self.cap.compute(cache=Key.object_cache)
        self.slot.compute(basis_face=self.cap.get_cad_object().faces("<Z"),
                          do_fill=self.base.is_filled,
                          cache=Key.object_cache)
        if DEBUG.render_switch:
            self.switch.compute()
        # translate cad objects to final position
        self.final_post_compute()

        self.expose_cad_objects()

    def expose_cad_objects(self):
        self.cad_objects.plane = self.base.get_cad_object()
        self.cad_objects.cap = self.cap.get_cad_object()
        self.cad_objects.slot = self.slot.get_cad_object()
        self.cad_objects.switch = self.switch.get_cad_object() if self.switch.has_cad_object() else None

        self.cad_objects.connectors.clear()
        to_expose = [self.connectors.front, self.connectors.right]
        for connector in [connector for connector in to_expose if connector.has_cad_object()]:
            self.cad_objects.connectors.append(connector.get_cad_object())
