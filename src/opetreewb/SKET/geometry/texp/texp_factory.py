import FreeCAD

from .texp_object import TexpObject
from .texp_view import ViewProviderTexp


def create_texp_object(node, doc):

    FreeCAD.Console.PrintMessage(
        f"[TEXT_FACTORY] Creating TEXT for node {node.node_id}\n"
    )

    obj = doc.addObject("App::FeaturePython", "TEXT")
    obj.Label = f"TEXT {node.node_id}"

    TexpObject(obj, node)
    ViewProviderTexp(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj