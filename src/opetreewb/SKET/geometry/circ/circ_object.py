class CircObject:
    def __init__(self, obj, node):

        obj.Proxy = self
        self.node = node

        obj.Proxy.node = node  # ✅ required for ViewProvider

        # ✅ geometry properties
        obj.addProperty("App::PropertyFloat", "CenterX", "Geometry")
        obj.addProperty("App::PropertyFloat", "CenterY", "Geometry")
        obj.addProperty("App::PropertyFloat", "Radius", "Geometry")

    def execute(self, obj):

        import FreeCAD

        FreeCAD.Console.PrintMessage(f"[CIRC_EXECUTE] node={self.node.node_id}\n")

        node = self.node

        def get_val(name, default=0.0):
            attr = node.attributes.get(name)
            if attr and attr.value is not None:
                try:
                    return float(attr.value)
                except Exception:
                    return default
            return default

        cx = get_val("CenterX", 0.0)
        cy = get_val("CenterY", 0.0)
        r = get_val("Radius", 5.0)

        obj.CenterX = cx
        obj.CenterY = cy
        obj.Radius = r

        # ✅ trigger view update
        if hasattr(obj.ViewObject, "Proxy") and hasattr(obj.ViewObject.Proxy, "update"):
            obj.ViewObject.Proxy.update(obj)
