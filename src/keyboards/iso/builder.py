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

    do_unify = kwargs.get('do_unify', False)

    # 1.
    key_matrix = build_key_matrix()

    # 2.
    apply_orientation_offset(key_matrix)
    apply_translation_offset(key_matrix)

    # 3.
    compute_placement_and_cad_objects(key_matrix)

    # 4.
    conn_map = get_key_face_connection_mapping(key_matrix)
    KeyUtils.connect_keys_face(key_matrix, conn_map)

    conn_map = get_key_corner_edge_connection_mapping(key_matrix)
    KeyUtils.connect_key_corner_edges(key_matrix, conn_map)

    # n.
    KeyUtils.filter_cad_objects(key_matrix, remove_non_solids=do_unify)

    return key_matrix
