import FreeCAD

from .circ_object import CircObject
from .circ_view import ViewProviderCirc


def create_circ_object(node, doc):

    FreeCAD.Console.PrintMessage(
        f"[CIRC_FACTORY] Creating circle for node {node.node_id}\n"
    )

    obj = doc.addObject("App::FeaturePython", "CIRC")
    obj.Label = f"CIRC {node.node_id}"

    CircObject(obj, node)
    ViewProviderCirc(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj
