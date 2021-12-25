from enum import Enum


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class KeyboardSize(Enum):
    """
    KeyboardSize.S100 : a planar ISO model would be inclusive f-row, number-row, arrow keys, pg-up/down group and numpad
    KeyboardSize.S80  : a planar ISO model would be inclusive f-row, number-row, arrow keys, pg-up/down group
    KeyboardSize.S75  : a planar ISO model would be inclusive f-row, number-row, ins/del, home/end, pg-up/down
    KeyboardSize.S65  : a planar ISO model would be inclusive number-row, del, home, pg-up/down
    KeyboardSize.S60  : a planar ISO model would be inclusive number-row
    KeyboardSize.S40  : a planar ISO model would be mainly characters
    """
    S100 = 100
    S80 = 80
    S75 = 75
    S65 = 65
    S60 = 60
    S40 = 40
