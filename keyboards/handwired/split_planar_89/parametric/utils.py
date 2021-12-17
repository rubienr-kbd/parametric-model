from keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyUtils(object):

    @staticmethod
    def set_position_relative_to(key: KeyBase, ref_key: KeyBase, pos: Direction) -> None:
        """
        Defines the key position as top/bottom left/right of the reference key.
        """
        if pos == Direction.TOP:
            key.position[1] = ref_key.position[1] + ref_key.depth / 2 + ref_key.clearance_top + key.clearance_bottom + key.depth / 2
            key.position[0] = ref_key.position[0]
        elif pos == Direction.BOTTOM:
            key.position[1] = ref_key.position[1] - ref_key.depth / 2 - ref_key.clearance_bottom - key.clearance_top - key.depth / 2
            key.position[0] = ref_key.position[0]

        elif pos == Direction.RIGHT:
            key.position[0] = ref_key.position[0] + ref_key.width / 2 + ref_key.clearance_right + key.clearance_left + key.width / 2
            key.position[1] = ref_key.position[1]
        elif pos == Direction.LEFT:
            key.position[0] = ref_key.position[0] - ref_key.width / 2 - ref_key.clearance_left - key.clearance_right - key.width / 2
            key.position[1] = ref_key.position[1]

        else:
            assert False
