from typing import Optional, Tuple, Dict

from cadquery import Shape
from config import *
from key_mixins import *
import cadquery

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


  Illustratoin of base plane, key and origin:

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

    def __init__(self, config: DebugConfig):
        self.container = dict()  # type: Dict[str, cadquery.Workplane]
        self.enabled = not config.disable_object_cache

    @staticmethod
    def cache_name(attr_1: str, attr_2: str = "0", attr_3: str = "0") -> str:
        return "{}-{}-{}".format(attr_1, attr_2, attr_3)

    def store(self, obj: cadquery.Workplane, attr_1: str, attr_2: str = "0", attr_3: str = "0") -> None:
        if not self.enabled:
            return

        key = ObjectCache.cache_name(attr_1, attr_2, attr_3)

        if key in self.container:
            print("failed to cache object with id {}".format(key))
            assert False
        self.container[key] = obj

    def get(self, attr_1: str, attr_2: str = "0", attr_3: str = "0") -> Optional[cadquery.Workplane]:
        if not self.enabled:
            return None
        else:
            key = ObjectCache.cache_name(attr_1, attr_2, attr_3)
            if key in self.container:
                return self.container[key] if key in self.container else None


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyBase(KeyPlane, Computeable, CadObject, KeyBaseMixin):
    def __init__(self, config: KeyBaseConfig) -> None:
        super(KeyBase, self).__init__()
        self.unit_length = config.unit_length  # type: float
        self.unit_width_factor = 1  # type: float
        self.unit_depth_factor = 1  # type: float
        self.clearance_left = config.clearance_x  # type: float
        self.clearance_right = config.clearance_x  # type: float
        self.clearance_top = config.clearance_y  # type: float
        self.clearance_bottom = config.clearance_y  # type: float
        self.is_visible = True  # type: bool

    def update(self) -> None:
        self.width = self.unit_width_factor * self.unit_length
        self.depth = self.unit_depth_factor * self.unit_length


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KeyCap(KeyBox, Computeable, CadObject):
    def __init__(self, config: KeyCapConfig) -> None:
        super(KeyCap, self).__init__()
        self.width_clearance = config.width_clearance  # type: float
        self.depth_clearance = config.depth_clearance  # type: float
        self.thickness = config.thickness  # type: float
        self.z_clearance = config.z_clearance  # type: float
        self.dish_inset = config.dish_inset  # type: float
        self.width = 0  # type: float
        self.depth = 0  # type: float

    def update(self, unit_width_factor: float = 1, unit_depth_factor: float = 1, unit_length: float = GlobalConfig.key_base.unit_length, *args, **kwargs) -> None:
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


class KeySwitch(KeyBox, Computeable, CadObject):

    def __init__(self, config: KeySwitchConfig) -> None:
        super(KeySwitch, self).__init__()
        self.width = config.width  # type: float
        self.depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeySwitchSlot(KeyBox, Computeable, CadObject):
    def __init__(self, config: KeySwitchSlotConfig) -> None:
        super(KeySwitchSlot, self).__init__()
        self.slot_width = config.width  # type: float
        self.slot_depth = config.depth  # type: float
        self.thickness = config.thickness  # type: float
        self.undercut_depth = config.undercut_depth  # type: float
        self.undercut_width = config.undercut_width  # type: float
        self.undercut_thickness = config.undercut_thickness  # type: float

    def compute(self, basis_face: cadquery.Workplane, cache: ObjectCache, *args, **kwargs) -> None:
        """
        To ensure the key cap clearance in cse keys are not placed planar,
        we use the key cap footprint as base size for the key slot.

        @precondition: key cap cad object has been computed
        @param basis_face: the bottom face of the key cap
        @param cache: container for lookup or storing
        """

        vs = basis_face.edges("|X").first().vertices("<X").first().val().X
        ve = basis_face.edges("|X").first().vertices(">X").first().val().X
        width = ve - vs
        cached = cache.get("slot", str(width), str(self.slot_depth))
        if cached is None:
            z_offset = basis_face.vertices(">Z").first().val().Z

            top = cadquery.Workplane().sketch() \
                .face(basis_face.wires().first().val()).faces("<Z") \
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
                .finalize().extrude(-self.thickness)

            self._cad_object = top.union(bottom.cut(undercut))
            cache.store(self._cad_object, "slot", str(width), str(self.slot_depth))
        else:
            self._cad_object = cache.get("slot", str(width), str(self.slot_depth))

    def get_cad_corner(self, direction_y: Direction, direction_x: Direction) -> cadquery.Workplane:
        if direction_y is Direction.BACK:
            if direction_x is Direction.LEFT:
                return self._cad_object.vertices(">Y and <X")
            elif direction_x is Direction.RIGHT:
                return self._cad_object.vertices(">Y and >X")
            else:
                assert False
        elif direction_y is Direction.FRONT:
            if direction_x is Direction.RIGHT:
                return self._cad_object.vertices("<Y and >X")
            elif direction_x is Direction.LEFT:
                return self._cad_object.vertices("<Y and <X")
            else:
                assert False
        else:
            assert False

    def get_cad_face(self, direction: Direction) -> cadquery.Workplane:
        if direction is Direction.FRONT:
            return self._cad_object.faces("|Z and |X and <Y")
        elif direction is Direction.BACK:
            return self._cad_object.faces("|Z and |X and >Y")
        elif direction is Direction.LEFT:
            return self._cad_object.faces("|Z and |Y and <X")
        elif direction is Direction.RIGHT:
            return self._cad_object.faces("|Z and |Y and >X")
        else:
            assert False


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CadObjects(object):
    def __init__(self):
        self.plane = None  # type: Optional[Shape]
        self.origin = None  # type: Optional[Shape]
        self.name = None  # type: Optional[Shape]
        self.cap = None  # type: Optional[Shape]
        self.slot = None  # type: Optional[Shape]
        self.switch = None  # type: Optional[Shape]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Key(Computeable, CadKeyMixin):
    object_cache = ObjectCache(GlobalConfig.debug)

    def __init__(self) -> None:
        self.base = KeyBase(GlobalConfig.key_base)
        self.cap = KeyCap(GlobalConfig.cap)
        self.slot = KeySwitchSlot(GlobalConfig.switch_slot)
        self.switch = KeySwitch(GlobalConfig.switch)
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
        self.slot.compute(basis_face=self.cap.get_cad_object().faces("<Z"), cache=Key.object_cache)
        self.switch.compute()

        # translate cad objects to final position
        self.final_post_compute()
        self.expose_cad_objects()

    def expose_cad_objects(self):
        if GlobalConfig.debug.show_placement:
            self.cad_objects.plane = self.base.get_cad_object()
        if GlobalConfig.debug.render_key_cap:
            self.cad_objects.cap = self.cap.get_cad_object()
        self.cad_objects.slot = self.slot.get_cad_object()
        if GlobalConfig.debug.render_key_switch:
            self.cad_objects.switch = self.switch.get_cad_object()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
