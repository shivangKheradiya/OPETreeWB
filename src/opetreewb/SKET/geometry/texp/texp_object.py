class TexpObject:

    def __init__(self, obj, node):

        obj.Proxy = self
        self.node = node

        obj.Proxy.node = node  # ✅ required

        # ✅ text properties
        obj.addProperty("App::PropertyString", "Text", "Text")
        obj.addProperty("App::PropertyFloat", "X", "Position")
        obj.addProperty("App::PropertyFloat", "Y", "Position")
        obj.addProperty("App::PropertyFloat", "FontSize", "Text")

    def execute(self, obj):

        import FreeCAD

        FreeCAD.Console.PrintMessage(
            f"[TEXT_EXECUTE] node={self.node.node_id}\n"
        )

        node = self.node

        def get_val(name, default):
            attr = node.attributes.get(name)
            if attr and attr.value is not None:
                return attr.value
            return default

        obj.Text = str(get_val("Text", "Text"))
        obj.X = float(get_val("X", 0.0))
        obj.Y = float(get_val("Y", 0.0))
        obj.FontSize = float(get_val("FontSize", 12))

        # ✅ trigger view update
        if hasattr(obj.ViewObject, "Proxy") and hasattr(obj.ViewObject.Proxy, "update"):
            obj.ViewObject.Proxy.update(obj)
