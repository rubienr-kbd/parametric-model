class DebugConfig(object):
    def __init__(self):
        """
        Configuration fot enable/disable features/items for development.

        Note: unified vs unified + clean vs assembly:
          assembly:        about 10 seconds
          unified:         about  1 minute
          unified + clean: about 10 minutes

        self.debug_enable: global switch to enable ir disable debug

        self.show_placement: outline the key placement for each key
        self.show_key_origin: outline each key origin (x/y-center) by a small circle
        self.show_key_name: renders the key name in the placement face
        self.show_key_cap: renders the key cap
        self.show_key_switch: renders the key switch (optional, only decorative)

        self.show_invisibles: force render placeholder components
        self.hide_slots: removes all slots from export/view
        self.hide_connectors: removes all connectors from export/view

        self.unify_in_cadquery_editor: unifies otherwise assemblies the rendered view; False recommended
        self.unify_in_step_export: unifies otherwise assemblies the rendered view; if True slower else very fast; True recommended
        self.do_clean_union_in_cadquery: to have a clean shape union; very slow if True else faster; False recommended
        self.do_clean_union_in_step_export: to have a clean shape union; very slow if True else faster; False recommended for freecad

        self.disable_object_cache: deactivate cad object caching, otherwise re-use pre-computed objects whenever possible; False recommended
        """

        self.debug_enable = True  # type: bool

        self.show_placement = False  # type: bool
        self.show_key_origin = False  # type: bool
        self.show_key_name = True  # type: bool
        self.show_key_cap = False  # type: bool
        self.show_key_switch = False  # type: bool

        self.show_invisibles = False  # type: bool
        self.hide_slots = False  # type: bool
        self.hide_connectors = False  # type: bool

        self.unify_in_cadquery_editor = False  # type: bool
        self.unify_in_step_export = True  # type: bool
        self.do_clean_union_in_cadquery = False  # type: bool
        self.do_clean_union_in_step_export = False  # type: bool

        self.disable_object_cache = False  # type: bool

    @property
    def render_placement(self):
        return self.debug_enable and self.show_placement

    @property
    def render_origin(self):
        return self.debug_enable and self.show_key_origin

    @property
    def render_name(self):
        return self.debug_enable and self.show_key_name

    @property
    def render_cap(self):
        return self.debug_enable and self.show_key_cap

    @property
    def render_invisibles(self):
        return self.debug_enable and self.show_invisibles

    @property
    def render_switch(self):
        return self.debug_enable and self.show_key_switch

    @property
    def render_slots(self):
        return True if not self.debug_enable else not self.hide_slots

    @property
    def render_connectors(self):
        return True if not self.debug_enable else not self.hide_connectors

    @property
    def render_unified(self):
        return self.unify_in_cadquery_editor

    @property
    def export_unified(self):
        return self.unify_in_step_export

    @property
    def render_cleaned_union(self):
        return self.do_clean_union_in_cadquery

    @property
    def export_cleaned_union(self):
        return self.do_clean_union_in_step_export


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

DEBUG = DebugConfig()
