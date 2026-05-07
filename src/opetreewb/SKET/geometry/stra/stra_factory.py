import FreeCAD

from .stra_object import StraObject
from .stra_view import ViewProviderStra


def create_stra_object(node, doc):

    FreeCAD.Console.PrintMessage(
        f"[STRA_FACTORY] Creating STRA object for node {node.node_id}\n"
    )
    
    obj = doc.addObject("App::FeaturePython", "STRA")
    obj.Label = f"STRA {node.node_id}"

    StraObject(obj, node)
    ViewProviderStra(obj.ViewObject)

    return obj
