import FreeCAD
from .elli_object import ElliObject
from .elli_view import ViewProviderElli


def create_elli_object(node, doc):

    obj = doc.addObject("App::FeaturePython", "ELLI")

    ElliObject(obj, node)
    ViewProviderElli(obj.ViewObject)

    obj.addProperty("App::PropertyInteger", "node_id")
    obj.node_id = node.node_id

    return obj