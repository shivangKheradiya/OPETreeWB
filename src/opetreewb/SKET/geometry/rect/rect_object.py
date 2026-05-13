class RectObject:

    def __init__(self, obj, node):

        obj.Proxy = self
        self.node = node
        obj.Proxy.node = node  # ✅ required

        # ✅ geometry properties
        obj.addProperty("App::PropertyFloat", "X", "Geometry")
        obj.addProperty("App::PropertyFloat", "Y", "Geometry")
        obj.addProperty("App::PropertyFloat", "Width", "Geometry")
        obj.addProperty("App::PropertyFloat", "Height", "Geometry")

    def execute(self, obj):

        import FreeCAD

        FreeCAD.Console.PrintMessage(
            f"[RECT_EXECUTE] node={self.node.node_id}\n"
        )

        node = self.node

        def get_val(name, default):
            attr = node.attributes.get(name)
            if attr and attr.value is not None:
                try:
                    return float(attr.value)
                except Exception:
                    return default
            return default

        obj.X = get_val("X", 0.0)
        obj.Y = get_val("Y", 0.0)
        obj.Width = get_val("Width", 10.0)
        obj.Height = get_val("Height", 5.0)

        # ✅ trigger render update
        obj.ViewObject.Proxy.update(obj)
