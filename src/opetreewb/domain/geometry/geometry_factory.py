"""
Geometry Factory

Maps node TYPE → geometry implementation
"""

def create_geometry(node, doc):
    """
    Create FreeCAD geometry object for a given node
    """

    type_name = node.type

    # -------------------------------------------------
    # LINE (STRA)
    # -------------------------------------------------
    if type_name == "STRA":
        try:
            from opetreewb.SKET.geometry.stra.stra_factory import create_stra_object
            return create_stra_object(node, doc)
        except Exception:
            return None

    # -------------------------------------------------
    # RECT (future)
    # -------------------------------------------------
    elif type_name == "RECT":
        # TODO: implement rectangle geometry later
        return None

    # -------------------------------------------------
    # CIRC (future)
    # -------------------------------------------------
    elif type_name == "CIRC":
        # TODO: implement circle
        return None

    # -------------------------------------------------
    # OUTL (hierarchical geometry)
    # -------------------------------------------------
    elif type_name == "OUTL":
        # Will be handled later (VRTX-based)
        return None

    # -------------------------------------------------
    # DEFAULT
    # -------------------------------------------------
    return None
