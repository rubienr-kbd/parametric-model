from typing import List

from .iso_matrix import *

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def compute(**kwargs) -> List[List[Key]]:
    """
    strategy
      1. assemble key matrix: define key size and style (iso, ansi, with or without numpad/arrows etc.), position and rotation
      2. optional: compute additional offsets rotation offset if keyboard is not planar
         a. position offset
         b. orientation offset
         c. rotation offset
      3. compute real key placement and cad objects
      4. connect keys (split keyboard: not yet supported)
      5. construct wall around keys (not yet supported)
      6. construct bottom plate (not yet supported)
      ...
      n. clean up cad objects that shall not be rendered
    """

    # 1.
    key_matrix = build_key_matrix()

    # 2.
    apply_translation_offset(key_matrix)
    # apply_orientation_offset(key_matrix)
    # apply_rotation_offset(key_matrix)

    # 3.
    compute_placement_and_cad_objects(key_matrix)

    # 4.
    conn_map = get_key_face_connection_mapping(key_matrix)
    KeyUtils.connect_keys_face(conn_map, key_matrix)

    conn_map = get_key_corner_edge_connection_mapping(key_matrix)
    KeyUtils.connect_key_corner_edges(conn_map, key_matrix)

    # n.
    kwargs.get('for_export', False)
    KeyUtils.remove_cad_objects(key_matrix, remove_non_solids=kwargs.get('for_export', False))

    return key_matrix
