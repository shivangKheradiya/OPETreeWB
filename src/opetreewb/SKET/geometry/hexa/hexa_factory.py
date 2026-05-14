import FreeCAD

from .hexa_object import HexaObject
from .hexa_view import ViewProviderHexa


def create_hexa_object(node, doc):

    obj = doc.addObject("App::FeaturePython", "HEXA")

    HexaObject(obj, node)
    ViewProviderHexa(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj
