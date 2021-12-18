from typing import Union, List
from enum import Enum

import cadquery


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    FRONT = 5
    BACK = 6


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Computeable(object):

    def update(self) -> None:
        """
        Resolves/computes input data dependencies for compute().
        """
        pass

    def compute(self) -> None:
        """
        Computes object and cad object
        """
        if hasattr(self, "width") and hasattr(self, "depth"):
            if hasattr(self, "thickness"):
                self._cad_object = cadquery.Workplane().box(self.width, self.depth, self.thickness)
            else:
                self._cad_object = cadquery.Workplane().rect(self.width, self.depth)
        else:
            assert False


class CadObject(object):
    def get_cad_object(self: Computeable) -> cadquery.Workplane:
        """
        If not re-implemented returns a bounding rect/box of the object.
        """
        assert hasattr(self, "_cad_object") and self._cad_object is not None
        return self._cad_object


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyRect(object):
    def __init__(self):
        self.width = 0.0  # type: float
        self.depth = 0.0  # type: float


class KeyBox(KeyRect):
    def __init__(self):
        super(KeyBox, self).__init__()
        self.thickness = 0.0  # type: float


class KeyPlane(KeyRect):
    def __init__(self):
        super(KeyPlane, self).__init__()
        self.position = [0.0, 0.0, 0.0]  # type: List[float, float, float]
        self.position_offset = [0.0, 0.0, 0.0]  # type: List[float, float, float]
        self.rotation = [0.0, 0.0, 0.0]  # type: List[float, float, float]
        self.rotation_offset = [0.0, 0.0, 0.0]  # type: List[float, float, float]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KeyBaseMixin(object):

    def align_to_position(self: Union[KeyPlane, KeyBox], position: float, pos: Direction) -> None:
        """
        Aligns our bounding box top/bottom left/right front/top to position (x, y or z-axis).
        """
        if pos == Direction.TOP:
            self.position[2] = position - self.thickness / 2
        elif pos == Direction.BOTTOM:
            self.position[2] = position + self.thickness / 2
        elif pos == Direction.RIGHT:
            self.position[0] = position - self.width / 2
        elif pos == Direction.LEFT:
            self.position[0] = position + self.width / 2
        elif pos == Direction.FRONT:
            self.position[1] = position + self.depth / 2
        elif pos == Direction.BACK:
            self.position[1] = position - self.depth / 2


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CadKeyMixin(object):

    def post_compute_cad_key_base(self) -> None:
        self.key_base._cad_object = self.key_base.get_cad_object() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("key_base" if self.key_base.is_visible else "key_base_invisible"))

    def post_compute_key_base_name(self) -> cadquery.Workplane:
        return self.key_base.get_cad_object().faces().text(self.name, 5, 1).faces("<Z") \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("name" if self.key_base.is_visible else "name_invisible"))

    def post_compute_cad_cap(self) -> None:
        self.cap._cad_object = self.cap.get_cad_object() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("cap" if self.key_base.is_visible else "cap_invisible"))

    def post_compute_cad_switch(self) -> None:
        self.switch._cad_object = self.switch.get_cad_object() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("switch" if self.key_base.is_visible else "switch_invisible"))

    def post_compute_cad_switch_slot(self) -> None:
        self.switch_slot._cad_object = self.switch_slot.get_cad_object() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("switch_slot" if self.key_base.is_visible else "switch_slot_invisible"))
