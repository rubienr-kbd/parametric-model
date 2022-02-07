from __future__ import annotations

import operator
from cmath import sqrt
from typing import TYPE_CHECKING, Union, List, Tuple, Optional
from enum import Enum
import cadquery

if TYPE_CHECKING:
    from .key import Key

from src.cfg.debug import DEBUG


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Direction(Enum):
    """
    Direction hints as seen from the keyboard user perspective.
    """

    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    FRONT = 5
    BACK = 6
    FRONT_LEFT = 7
    FRONT_RIGHT = 8
    BACK_LEFT = 9
    BACK_RIGHT = 10


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

    def update(self: Union[Computeable, CadObject], *_args, **_kwargs) -> None:
        """
        Resolves/computes input data dependencies for a subsequent compute().
        """
        pass

    def compute(self: Union[Computeable, CadObject], *_args, **_kwargs) -> None:
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
        self._cad_object = None  # type: Optional[cadquery.Workplane]

    def has_cad_object(self: Computeable, *_args, **_kwargs) -> bool:
        return hasattr(self, "_cad_object") and self._cad_object is not None

    def get_cad_object(self: Union[Computeable, CadObject], *_args, **_kwargs) -> cadquery.Workplane:
        """
        If not re-implemented returns the pre-computed _cad_object property.
        """
        assert self.has_cad_object()
        return self._cad_object

    def set_cad_object(self: Union[Computeable, CadObject], cad_object: cadquery.Workplane, *_args, **_kwargs) -> None:
        self._cad_object = cad_object


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CartesianRoot(object):
    """
    The cartesian root is used to track translation/rotation.
    It is a relative anchor for objects that are displaced from the absolute cartesian root and is mainly used for CadQuery selectors where the normals relative to the object are needed.

    The axes vectors are relative to the global coordinate system's origin (not to relative to the relative origin).
    The axes vectors must be orthogonal altogether.
    The axes vectors will be normed upon assignment.
    """

    def __init__(self):
        self.origin = (0, 0, 0)
        self._x_axis = (1, 0, 0)
        self._y_axis = (0, 1, 0)
        self._z_axis = (0, 0, 1)
        self._xy_normal = self._z_axis
        self._yz_normal = self._x_axis
        self._zx_normal = self._y_axis

    @property
    def x_axis(self) -> Tuple[float, float, float]:
        return self._x_axis

    @property
    def y_axis(self) -> Tuple[float, float, float]:
        return self._y_axis

    @property
    def z_axis(self) -> Tuple[float, float, float]:
        return self._z_axis

    @x_axis.setter
    def x_axis(self, value: Tuple[float, float, float]) -> None:
        self._x_axis = self._normalize_vector(value)

    @y_axis.setter
    def y_axis(self, value: Tuple[float, float, float]) -> None:
        self._y_axis = self._normalize_vector(value)

    @z_axis.setter
    def z_axis(self, value: Tuple[float, float, float]) -> None:
        self._z_axis = self._normalize_vector(value)

    @property
    def xy_normal(self) -> Tuple[float, float, float]:
        return self._xy_normal

    @property
    def yz_normal(self) -> Tuple[float, float, float]:
        return self._yz_normal

    @property
    def zx_normal(self) -> Tuple[float, float, float]:
        return self._zx_normal

    def update_axes(self, x: Tuple[float, float, float], y: Tuple[float, float, float], z: Tuple[float, float, float]) -> None:
        """
        Set new xyz axis: normalize axis, compute normals and check the orthogonality.
        """
        self.x_axis = x
        self.y_axis = y
        self.z_axis = z
        self._compute_normals()

    def _compute_normals(self):
        self._assert_orthogonality()
        self._xy_normal = self.z_axis
        self._yz_normal = self.x_axis
        self._zx_normal = self.y_axis

    @staticmethod
    def _normalize_vector(axis: Tuple[float, float, float]) -> Tuple[float, float, float]:
        length = sqrt(axis[0] * axis[0] + axis[1] * axis[1] + axis[2] * axis[2])
        assert length.imag == 0.0
        factor = 1.0 / length.real
        return factor * axis[0], factor * axis[1], factor * axis[2]

    def _assert_orthogonality(self, allowed_error: float = 0.001):
        def product(v1: Tuple[float, float, float], v2: Tuple[float, float, float]) -> float:
            return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

        p = product(self.x_axis, self.y_axis)
        assert -allowed_error < p < allowed_error, "product x * y is not 0: {} * {} = {}".format(self.x_axis, self.y_axis, p)
        p = product(self.y_axis, self.z_axis)
        assert -allowed_error < p < allowed_error, "product y * z is not 0: {} * {} = {}".format(self.y_axis, self.z_axis, p)
        p = product(self.z_axis, self.x_axis)
        assert -allowed_error < p < allowed_error, "product z * x is not 0: {} * {} = {}".format(self.z_axis, self.x_axis, p)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyRect(object):
    """
    Rectangular 2D plane.
    """

    def __init__(self):
        self.width = 0  # type: float
        self.depth = 0  # type: float


class KeyBox(KeyRect):
    """
    3D box.
    """

    def __init__(self):
        super(KeyBox, self).__init__()
        self.thickness = 0  # type: float


class KeyPlane(KeyRect):
    ABSOLUTE_CARTESIAN = CartesianRoot()

    def __init__(self):
        """
        self.x_axis: x_axis vector relative to object (considers self.rotation + self.rotation_offset)
        self.y_axis: y_axis vector relative to object (considers self.rotation + self.rotation_offset)
        self.z_axis: z_axis vector relative to object (considers self.rotation + self.rotation_offset)
        """
        super(KeyPlane, self).__init__()
        self.position = (0, 0, 0)  # type: Tuple[float, float, float]
        self.position_offset = (0, 0, 0)  # type: Tuple[float, float, float]
        self.rotation = (0, 0, 0)  # type: Tuple[float, float, float]
        self.rotation_offset = (0, 0, 0)  # type: Tuple[float, float, float]
        self.relative_cartesian = CartesianRoot()

    @property
    def total_translation(self) -> Tuple[float, float, float]:
        return (self.position[0] + self.position_offset[0],
                self.position[1] + self.position_offset[1],
                self.position[2] + self.position_offset[2])

    @property
    def total_rotation(self) -> Tuple[float, float, float]:
        return (self.rotation[0] + self.rotation_offset[0],
                self.rotation[1] + self.rotation_offset[1],
                self.rotation[2] + self.rotation_offset[2])

    def compute_relative_cardinal_translation(self) -> None:
        """
        Updates the relative cartesian origin according to the total translation (position + position_offset).
        """
        self.relative_cartesian.origin = tuple(map(operator.add, self.position, self.position_offset))

    def compute_relative_cardinal_rotation(self) -> None:
        """
        Updates the relative cartesian vectors according to the total rotation (rotation + rotation_offset).
        Note: the computation misuses CadQuery for sake of laziness.
        """

        rx, ry, rz = self.total_rotation
        cq_origin = cadquery.Vector(self.ABSOLUTE_CARTESIAN.origin)
        cq_vec_x, cq_vec_y, cq_vec_z = cadquery.Vector(self.ABSOLUTE_CARTESIAN.x_axis), cadquery.Vector(self.ABSOLUTE_CARTESIAN.y_axis), cadquery.Vector(self.ABSOLUTE_CARTESIAN.z_axis)
        cq_line_x = cadquery.Edge.makeLine(cq_origin, cq_vec_x)
        cq_line_y = cadquery.Edge.makeLine(cq_origin, cq_vec_y)
        cq_line_z = cadquery.Edge.makeLine(cq_origin, cq_vec_z)

        line_x = cq_line_x.rotate(cq_origin, cq_vec_z, rz).rotate(cq_origin, cq_vec_x, rx).rotate(cq_origin, cq_vec_y, ry)
        line_y = cq_line_y.rotate(cq_origin, cq_vec_z, rz).rotate(cq_origin, cq_vec_x, rx).rotate(cq_origin, cq_vec_y, ry)
        line_z = cq_line_z.rotate(cq_origin, cq_vec_z, rz).rotate(cq_origin, cq_vec_x, rx).rotate(cq_origin, cq_vec_y, ry)

        self.relative_cartesian.update_axes(line_x.tangentAt(0).toTuple(), line_y.tangentAt(0).toTuple(), line_z.tangentAt(0).toTuple())


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class KeyBaseMixin(object):

    def align_to_position(self: Union[KeyPlane, KeyBox, KeyBaseMixin], position: float, pos: Direction) -> None:
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

    def post_compute_cad_key_base(self: Key) -> None:
        origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
        self.base._cad_object = self.base.get_cad_object() \
            .rotate(origin, relative.z_axis, rz) \
            .rotate(origin, relative.x_axis, rx) \
            .rotate(origin, relative.y_axis, ry) \
            .translate(tuple(self.base.total_translation))
        self.base._cad_object = self.base.get_cad_object()

    def post_compute_key_name(self: Key) -> cadquery.Workplane:
        o = self.object_cache.get("name", self.name)
        if o is None:
            origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
            o = self.base.get_cad_object().faces() \
                .text(self.name, 5, 1).faces("<Z").wires() \
                .rotate(origin, relative.z_axis, rz) \
                .rotate(origin, relative.x_axis, rx) \
                .rotate(origin, relative.y_axis, ry)
            self.object_cache.store(o, "name", self.name)

        return o.translate(tuple(self.base.total_translation))

    def post_compute_key_origin(self: Key) -> cadquery.Workplane:
        o = self.object_cache.get("origin", self.name)
        if o is None:
            origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
            o = self.base.get_cad_object().faces() \
                .circle(0.5).extrude(1).faces("<Z").edges("not %Line") \
                .rotate(origin, relative.z_axis, rz) \
                .rotate(origin, relative.x_axis, rx) \
                .rotate(origin, relative.y_axis, ry)
            self.object_cache.store(o, "origin", self.name)

        return o.translate(tuple(self.base.total_translation))

    def post_compute_cad_cap(self: Key):
        origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
        self.cap._cad_object = self.cap.get_cad_object() \
            .rotate(origin, relative.z_axis, rz) \
            .rotate(origin, relative.x_axis, rx) \
            .rotate(origin, relative.y_axis, ry) \
            .translate(tuple(self.base.total_translation))
        self.cap._cad_object = self.cap.get_cad_object()

    def post_compute_cad_slot(self: Key) -> None:
        origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
        self.slot._cad_object = self.slot.get_cad_object() \
            .rotate(origin, relative.z_axis, rz) \
            .rotate(origin, relative.x_axis, rx) \
            .rotate(origin, relative.y_axis, ry) \
            .translate(tuple(self.base.total_translation))
        self.slot._cad_object = self.slot.get_cad_object()

    def post_compute_cad_switch(self: Key) -> None:
        origin, relative, (rx, ry, rz) = self.base.ABSOLUTE_CARTESIAN.origin, self.base.relative_cartesian, self.base.total_rotation
        self.switch._cad_object = self.switch.get_cad_object() \
            .rotate(origin, relative.z_axis, rz) \
            .rotate(origin, relative.x_axis, rx) \
            .rotate(origin, relative.y_axis, ry) \
            .translate(tuple(self.base.total_translation))
        self.switch._cad_object = self.switch.get_cad_object()

    def final_post_compute(self: Key):
        self.post_compute_cad_key_base()

        if DEBUG.render_name:
            self.cad_objects.name = self.post_compute_key_name()
        if DEBUG.render_origin:
            self.cad_objects.origin = self.post_compute_key_origin()

        self.post_compute_cad_cap()
        self.post_compute_cad_slot()
        if self.switch.has_cad_object():
            self.post_compute_cad_switch()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class DactylAttributesMixin(object):

    def set_is_left_hand(self: Key) -> Union[Key, DactylAttributesMixin]:
        self.dactyl.is_left_hand = True
        return self

    def set_is_right_hand(self: Key) -> Union[Key, DactylAttributesMixin]:
        self.dactyl.is_left_hand = False
        return self

    def set_is_arrow_block(self: Key, is_arrow_block=True) -> Union[Key, DactylAttributesMixin]:
        self.dactyl.is_arrow_block = is_arrow_block
        return self

    def set_is_numpad_block(self: Key, is_numpad_block=True) -> Union[Key, DactylAttributesMixin]:
        self.dactyl.is_numpad_block = is_numpad_block
        return self
