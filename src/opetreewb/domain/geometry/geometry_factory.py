"""
Geometry Factory

Maps node TYPE → geometry implementation
"""

import FreeCAD

def create_geometry(node, doc):
    """
    Create FreeCAD geometry object for a given node
    """

    FreeCAD.Console.PrintMessage(
        "[Factory] Creating geometry for type={}\n".format(node.attributes.get("Type").value)
    )

    type_name = node.attributes.get("Type").value

    if type_name == "STRA":
        try:
            from opetreewb.SKET.geometry.stra.stra_factory import create_stra_object
            return create_stra_object(node, doc)
        except Exception:
            return None
    elif type_name == "RECT":
        try:
            from opetreewb.SKET.geometry.rect.rect_factory import create_rect_object
            return create_rect_object(node, doc)
        except Exception:
            return None
    elif type_name == "CIRC":
        try:
            from opetreewb.SKET.geometry.circ.circ_factory import create_circ_object
            return create_circ_object(node, doc)
        except Exception:
            return None
    elif type_name == "ARC":
        try:
            from opetreewb.SKET.geometry.arc.arc_factory import create_arc_object
            return create_arc_object(node, doc)
        except Exception:
            return None
    elif type_name == "ELLI":
        try:
            from opetreewb.SKET.geometry.elli.elli_factory import create_elli_object
            return create_elli_object(node, doc)
        except Exception:
            return None
    elif type_name == "TEXP":
        try:
            from opetreewb.SKET.geometry.texp.texp_factory import create_texp_object
            return create_texp_object(node, doc)
        except Exception:
            return None
    elif type_name == "HEXA":
        try:
            from opetreewb.SKET.geometry.hexa.hexa_factory import create_hexa_object
            return create_hexa_object(node, doc)
        except Exception:
            return None

    return None
