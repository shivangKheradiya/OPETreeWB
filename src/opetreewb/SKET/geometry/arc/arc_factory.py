import FreeCAD

from .arc_object import ArcObject
from .arc_view import ViewProviderArc


def create_arc_object(node, doc):

    obj = doc.addObject("App::FeaturePython", "ARC")

    ArcObject(obj, node)
    ViewProviderArc(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj
