import cadquery as cq
from isokeys import *


def build_key_row_0():  # space bar row
    r = [LeftCtrlKey(),
         LeftMenulKey(),
         LeftAltKey(),
         SpaceKey(),
         RightAltKey(),
         RightContextMenulKey(),
         RightCtrlKey(),
         ArrowLeftKey(),
         ArrowDownKey(),
         ArrowRightKey()]
    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_1():  # <yxc row
    r = [LeftShiftKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         RightShiftKey(),
         ArrowUpKey()]
    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_2():  # asdf row
    r = [CapsLockKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey()]
    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_3():  # qwer row
    r = [TabKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         IsoEnterKey(),
         DeleteKey(),
         EndKey(),
         PageDown()]
    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_4():  # number row
    r = [CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         CharacterKey(),
         BackspaceKey(),
         InsertKey(),
         HomeKey(),
         PageUpKey()]
    KeyUtils.update_key_pos_in_row(r)
    return r


def build_key_row_5():  # F row
    r = [EscapeKey(),
         F1Key(),
         CharacterKey(),
         CharacterKey(),
         F4Key(),
         F5Key(),
         CharacterKey(),
         CharacterKey(),
         F8Key(),
         F9Key(),
         CharacterKey(),
         CharacterKey(),
         F12Key(),
         PrintKey(),
         ScrollLockKey(),
         PauseKey()]
    KeyUtils.update_key_pos_in_row(r)
    return r


keys_matrix = [
    build_key_row_0(),
    build_key_row_1(),
    build_key_row_2(),
    build_key_row_3(),
    build_key_row_4(),
    build_key_row_5(),
]


o = cq.Workplane("XY")
last_row = None
last_key = None
for row in keys_matrix:

    print("")
    is_first_key_in_row = True
    for key in row:

        if is_first_key_in_row and last_row is not None:
            key.key_base.set_position_relative_to(last_row[0].key_base, Direction.TOP)
        elif last_key is not None:
            key.key_base.set_position_relative_to(last_key.key_base, Direction.RIGHT)
        is_first_key_in_row = False
        last_key = key

        show_object(o.box(key.cap.width, key.cap.depth, key.cap.thickness).translate(tuple(key.key_base.position)))
        print("{}".format(key.key_base.position))
    last_row = row

