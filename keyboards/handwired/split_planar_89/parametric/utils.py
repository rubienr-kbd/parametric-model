from keys import *


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyUtils(object):

    @staticmethod
    def set_position_relative_to(key: KeyBase, ref_key: KeyBase, pos: Direction) -> None:
        """
        Defines the key position as top/bottom left/right of the reference key.
        """
        position = None  # type: Optional[Tuple[float,float,float]]
        if pos == Direction.TOP:
            position = (
                ref_key.position[0],
                ref_key.position[1] + ref_key.depth / 2 + ref_key.clearance_top + key.clearance_bottom + key.depth / 2,
                key.position[2])

        elif pos == Direction.BOTTOM:
            position = (
                ref_key.position[0],
                ref_key.position[1] - ref_key.depth / 2 - ref_key.clearance_bottom - key.clearance_top - key.depth / 2,
                key.position[2])

        elif pos == Direction.RIGHT:
            position = (
                ref_key.position[0] + ref_key.width / 2 + ref_key.clearance_right + key.clearance_left + key.width / 2,
                ref_key.position[1],
                key.position[2])

        elif pos == Direction.LEFT:
            position = (
                ref_key.position[0] - ref_key.width / 2 - ref_key.clearance_left - key.clearance_right - key.width / 2,
                ref_key.position[1],
                key.position[2])

        else:
            assert False

        key.position = position
