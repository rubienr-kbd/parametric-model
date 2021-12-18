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

    def get_cad_key_base(self) -> cadquery.Workplane:
        key_base = self.key_base  # type: Union[KeyPlane, CadObject]
        return key_base.get_cad_object() \
            .translate(tuple(key_base.position)) \
            .translate(tuple(key_base.position_offset)) \
            .tag("{}".format("key_base" if key_base.is_visible else "key_base_invisible"))

    def get_cad_cap(self) -> cadquery.Workplane:
        cap = self.cap  # type: Union[KeyBox, CadObject]
        key_base = self.key_base  # type: KeyPlane
        return cap.get_cad_object() \
            .translate(tuple(key_base.position)) \
            .translate(tuple(key_base.position_offset)) \
            .tag("{}".format("cap" if key_base.is_visible else "cap_invisible"))

    def get_cad_switch(self) -> cadquery.Workplane:
        switch = self.switch  # type: Union[KeyBox, CadObject]
        key_base = self.key_base  # type: KeyPlane
        return switch.get_cad_object() \
            .translate(tuple(key_base.position)) \
            .translate(tuple(key_base.position_offset)) \
            .tag("{}".format("switch" if key_base.is_visible else "switch_invisible"))

    def get_cad_switch_slot(self) -> cadquery.Workplane:
        switch_slot = self.switch_slot  # type: Union[KeyBox, CadObject]
        key_base = self.key_base  # type: KeyPlane
        return switch_slot.get_cad_object() \
            .translate(tuple(key_base.position)) \
            .translate(tuple(key_base.position_offset)) \
            .tag("{}".format("switch_slot" if key_base.is_visible else "switch_slot_invisible"))
