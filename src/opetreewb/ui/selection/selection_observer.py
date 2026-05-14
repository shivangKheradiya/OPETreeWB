import FreeCAD
import FreeCADGui

from opetreewb.domain import CN
from opetreewb.domain.services.service_locator import get_geometry_service


class OPESelectionObserver:
    def addSelection(self, doc_name, obj_name, sub, pos):

        doc = FreeCAD.ActiveDocument
        if not doc:
            return

        obj = doc.getObject(obj_name)
        if not obj:
            return

        proxy = getattr(obj, "Proxy", None)

        if not proxy or not hasattr(proxy, "node_id"):
            return

        node_id = proxy.node_id

        FreeCAD.Console.PrintMessage(
            f"[Selection] Geometry selected → node_id={node_id}\n"
        )

        node = get_geometry_service().reverse_registry.get(obj.Name)

        if node:
            CN.set(node)
