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

    def update(self, *args, **kwargs) -> None:
        """
        Resolves/computes input data dependencies for compute().
        """
        pass

    def compute(self, *args, **kwargs) -> None:
        """
        Computes object and cad object
          - py object: noop
          - cad object: bounding rect/box of the object
        """
        if hasattr(self, "width") and hasattr(self, "depth"):
            if hasattr(self, "thickness"):
                self._cad_object = cadquery.Workplane().box(self.width, self.depth, self.thickness)
            else:
                self._cad_object = cadquery.Workplane().rect(self.width, self.depth)
        else:
            assert False


class CadObject(object):

    def __init__(self):
        self._cad_object = None

    def get_cad_object(self: Computeable, *args, **kwargs) -> cadquery.Workplane:
        """
        If not re-implemented returns the pre-computed _cad_object property.
        """
        assert hasattr(self, "_cad_object") and self._cad_object is not None
        return self._cad_object


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyRect(object):
    def __init__(self):
        self.width = 0  # type: float
        self.depth = 0  # type: float


class KeyBox(KeyRect):
    def __init__(self):
        super(KeyBox, self).__init__()
        self.thickness = 0  # type: float


class KeyPlane(KeyRect):
    def __init__(self):
        super(KeyPlane, self).__init__()
        self.position = (0, 0, 0)  # type: Tuple[float, float, float]
        self.position_offset = (0, 0, 0)  # type: Tuple[float, float, float]
        self.rotation = (0, 0, 0)  # type: Tuple[float, float, float]
        self.rotation_offset = (0, 0, 0)  # type: Tuple[float, float, float]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KeyBaseMixin(object):

    def align_to_position(self: Union[KeyPlane, KeyBox], position: float, pos: Direction) -> None:
        """
        Aligns our position top/bottom, left/right or front/top face to x (left/right), y (front/back) or z-axis (top/bottom).
        """
        result = list(self.position)  # type: List[float]

        if pos == Direction.TOP:
            result[2] = position - self.thickness / 2
        elif pos == Direction.BOTTOM:
            result[2] = position + self.thickness / 2

        elif pos == Direction.RIGHT:
            result[0] = position - self.width / 2
        elif pos == Direction.LEFT:
            result[0] = position + self.width / 2

        elif pos == Direction.FRONT:
            result[1] = position + self.depth / 2
        elif pos == Direction.BACK:
            result[1] = position - self.depth / 2
        else:
            assert False

        self.position = tuple(result)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CadKeyMixin(object):

    def post_compute_cad_key_base(self) -> None:
        self.key_base._cad_object = self.key_base.get_cad_object() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset)) \
            .tag("{}".format("key_base" if self.key_base.is_visible else "key_base_invisible"))

    @staticmethod
    def tag(cad_object: cadquery.Workplane, is_visible: bool, tag_text: str) -> cadquery.Workplane:
        return cad_object.tag("{}{}".format(tag_text, "_invisible" if not is_visible else ""))

    def post_compute_key_base_name(self) -> cadquery.Workplane:
        o = self.key_base.get_cad_object().faces().text(self.name, 5, 1).faces("<Z").wires() \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset))
        return CadKeyMixin.tag(o, self.key_base.is_visible, "name")

    def post_compute_key_base_origin(self) -> cadquery.Workplane:
        o = self.key_base.get_cad_object().faces().circle(0.5).extrude(1).faces("<Z").edges("not %Line") \
            .translate(tuple(self.key_base.position)) \
            .translate(tuple(self.key_base.position_offset))
        return CadKeyMixin.tag(o, self.key_base.is_visible, "origin")

    def post_compute_cad_cap(self):
        self.cap._cad_object = CadKeyMixin.tag(self.cap._cad_object, self.key_base.is_visible, "cap")

    def post_compute_cad_switch(self) -> None:
        self.switch._cad_object = CadKeyMixin.tag(self.cap._cad_object, self.key_base.is_visible, "switch")

    def post_compute_cad_switch_slot(self) -> None:
        self.switch_slot._cad_object = CadKeyMixin.tag(self.cap._cad_object, self.key_base.is_visible, "switch_slot")
