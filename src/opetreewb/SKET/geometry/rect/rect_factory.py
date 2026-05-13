import FreeCAD

from .rect_object import RectObject
from .rect_view import ViewProviderRect


def create_rect_object(node, doc):

    FreeCAD.Console.PrintMessage(
        f"[RECT_FACTORY] Creating rectangle for node {node.node_id}\n"
    )

    obj = doc.addObject("App::FeaturePython", "RECT")
    obj.Label = f"RECT {node.node_id}"

    RectObject(obj, node)
    ViewProviderRect(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj
