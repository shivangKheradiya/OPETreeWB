import FreeCAD

from opetreewb.domain.geometry.geometry_factory import create_geometry


class GeometryService:
    """
    Responsible for:
    - Building geometry for CN node and its hierarchy
    - Removing geometry
    - Updating geometry when attributes change
    """

    def __init__(self):
        # node_id → FreeCAD object
        self.registry = {}

    # -------------------------------------------------
    # BUILD GEOMETRY
    # -------------------------------------------------
    def build(self, node):

        doc = FreeCAD.ActiveDocument
        if doc is None:
            doc = FreeCAD.newDocument("OPE_3D_TEMP")

        self._build_recursive(node, doc)

        doc.recompute()

    def _build_recursive(self, node, doc):

        obj = create_geometry(node, doc)

        if obj:
            # ✅ store mapping
            self.registry[node.node_id] = obj

        # ✅ process children (hierarchical geometry)
        for child in node.children:
            self._build_recursive(child, doc)

    # -------------------------------------------------
    # REMOVE GEOMETRY
    # -------------------------------------------------
    def remove(self, node):

        doc = FreeCAD.ActiveDocument
        if not doc:
            return

        self._remove_recursive(node, doc)

        doc.recompute()

    def _remove_recursive(self, node, doc):

        obj = self.registry.get(node.node_id)

        if obj:
            try:
                doc.removeObject(obj.Name)
            except Exception:
                pass

            # ✅ remove from registry
            self.registry.pop(node.node_id, None)

        for child in node.children:
            self._remove_recursive(child, doc)

    # -------------------------------------------------
    # UPDATE GEOMETRY
    # -------------------------------------------------
    def update(self, node):

        obj = self.registry.get(node.node_id)

        if not obj:
            return

        # ✅ trigger recompute → execute() → ViewProvider update
        try:
            FreeCAD.ActiveDocument.recompute()
        except Exception:
            pass