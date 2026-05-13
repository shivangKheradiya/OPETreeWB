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
        self.reverse_registry = {}

    # -------------------------------------------------
    # BUILD GEOMETRY
    # -------------------------------------------------
    def build(self, node):

        FreeCAD.Console.PrintMessage(
            f"[GeometryService] Building geometry for node: {getattr(node, 'label', None)}\n"
        )

        doc = FreeCAD.ActiveDocument
        if doc is None:
            doc = FreeCAD.newDocument("OPE_3D_TEMP")

        self._build_recursive(node, doc)

        FreeCAD.Console.PrintMessage(
            "[GeometryService] Recompute triggered\n"
        )

        doc.recompute()

    def _build_recursive(self, node, doc):

        FreeCAD.Console.PrintMessage(
            f"[GeometryService] Visiting node: {node.label} (type={getattr(node, 'type', None)})\n"
        )

        node_id = node.node_id
        existing_obj = self.registry.get(node_id)

        if existing_obj:
            FreeCAD.Console.PrintMessage(
                f"[GeometryService] ✅ Already exists → skipping creation (node_id={node_id})\n"
            )
            return

        obj = create_geometry(node, doc)

        if obj:
            FreeCAD.Console.PrintMessage(
                f"[GeometryService] Geometry created for node_id={node.node_id}\n"
            )
            obj.Proxy.node_id = node.node_id
            self.registry[node.node_id] = obj
            self.reverse_registry[obj.Name] = node
        else:
            FreeCAD.Console.PrintMessage(
                f"[GeometryService] No geometry for type={getattr(node, 'type', None)}\n"
            )

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
            self.reverse_registry.pop(obj.Name, None)

        for child in node.children:
            self._remove_recursive(child, doc)

    # -------------------------------------------------
    # UPDATE GEOMETRY
    # -------------------------------------------------
    def update(self, node):
        FreeCAD.Console.PrintMessage(
            f"[GeometryService] Update called for node_id={node.node_id}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"[GeometryService] Registry keys: {list(self.registry.keys())}\n"
        )

        obj = self.registry.get(node.node_id)

        if not obj:
            FreeCAD.Console.PrintMessage(
                "[GeometryService] ❌ Object NOT found in registry\n"
            )
            return

        FreeCAD.Console.PrintMessage(
            "[GeometryService] ✅ Object found → recompute\n"
        )
        try:
            obj.touch()
            FreeCAD.ActiveDocument.recompute()
        except Exception:
            pass
