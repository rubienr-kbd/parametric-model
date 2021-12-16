import cadquery
import cadquery as cq


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CqBoxMixin(object):

    def get_cq_object(self) -> cadquery.Workplane:
        return cq.Workplane().box(self.width, self.depth, self.thickness)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CqKeyMixin(object):

    def get_cq_key_base(self) -> cadquery.Workplane:
        return self.key_base.get_cq_object().translate(tuple(self.key_base.position)).tag("{}".format("base" if self.key_base.is_visible else "b_invisible"))

    def get_cq_cap(self) -> cadquery.Workplane:
        return self.cap.get_cq_object().translate(tuple(self.key_base.position)).tag("{}".format("cap" if self.key_base.is_visible else "cap_invisible"))

    def get_cq_switch(self) -> cadquery.Workplane:
        return self.swith.get_cq_object().translate(tuple(self.key_base.position)).tag("{}".format("switch" if self.key_base.is_visible else "switch_invisible"))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyMixin(object):

    def set_key_width_unit_factor(self, unit_factor: float) -> None:
        self.key_base.unit_width_factor = unit_factor
        self.cap.width = self.key_base.width

    def set_key_depth_unit_factor(self, unit_factor: float) -> None:
        self.key_base.unit_depth_factor = unit_factor
        self.cap.depth = self.key_base.depth
