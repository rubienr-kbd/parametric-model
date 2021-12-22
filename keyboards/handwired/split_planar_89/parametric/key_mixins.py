from __future__ import annotations
from typing import Union, List, Tuple
from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from key import Key

import cadquery

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from config import GlobalConfig


class Direction(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    FRONT = 5
    BACK = 6


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class IterableObject(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            if value is None:
                continue
            else:
                yield attr, value

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

    def has_cad_object(self: Computeable, *args, **kwargs) -> bool:
        return hasattr(self, "_cad_object") and self._cad_object is not None

    def get_cad_object(self: Union[Computeable, "CadObject"], *args, **kwargs) -> cadquery.Workplane:
        """
        If not re-implemented returns the pre-computed _cad_object property.
        """
        assert self.has_cad_object()
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

    @staticmethod
    def tag(cad_object: cadquery.Workplane, is_visible: bool, tag_text: str) -> cadquery.Workplane:
        return cad_object.tag("{}{}".format(tag_text, "_invisible" if not is_visible else ""))

    def post_compute_cad_key_base(self: Key) -> None:
        self.base._cad_object = self.base.get_cad_object() \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))
        self.base._cad_object = CadKeyMixin.tag(self.base.get_cad_object(), self.base.is_visible, "key_base")

    def post_compute_key_name(self: Key) -> cadquery.Workplane:
        o = self.object_cache.get("name", self.name)
        if o is None:
            o = self.base.get_cad_object().faces() \
                .text(self.name, 5, 1).faces("<Z").wires()
            o = CadKeyMixin.tag(o, self.base.is_visible, "name")
            self.object_cache.store(o, "name", self.name)

        return o \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))

    def post_compute_key_origin(self: Key) -> cadquery.Workplane:
        o = self.object_cache.get("origin", self.name)
        if o is None:
            o = self.base.get_cad_object().faces() \
                .circle(0.5).extrude(1).faces("<Z").edges("not %Line")
            o = CadKeyMixin.tag(o, self.base.is_visible, "origin")
            self.object_cache.store(o, "origin", self.name)

        return o \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))

    def post_compute_cad_cap(self: Key):
        self.cap._cad_object = self.cap.get_cad_object() \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))
        self.cap._cad_object = CadKeyMixin.tag(self.cap.get_cad_object(), self.base.is_visible, "cap")

    def post_compute_cad_slot(self: Key) -> None:
        self.slot._cad_object = self.slot.get_cad_object() \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))
        self.slot._cad_object = CadKeyMixin.tag(self.slot.get_cad_object(), self.base.is_visible, "slot")

    def post_compute_cad_switch(self: Key) -> None:
        self.switch._cad_object = self.switch.get_cad_object() \
            .translate(tuple(self.base.position)) \
            .translate(tuple(self.base.position_offset))
        self.switch._cad_object = CadKeyMixin.tag(self.switch.get_cad_object(), self.base.is_visible, "switch")

    def final_post_compute(self: Key):
        self.post_compute_cad_key_base()

        if GlobalConfig.debug.render_name:
            self.cad_objects.name = self.post_compute_key_name()
        if GlobalConfig.debug.render_origin:
            self.cad_objects.origin = self.post_compute_key_origin()

        self.post_compute_cad_cap()
        self.post_compute_cad_slot()
        if self.switch.has_cad_object():
            self.post_compute_cad_switch()
