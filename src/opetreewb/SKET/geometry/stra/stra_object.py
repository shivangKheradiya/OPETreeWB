class StraObject:

    def __init__(self, obj, node):

        obj.Proxy = self
        self.node = node

        obj.addProperty("App::PropertyFloat", "StartX", "Geometry")
        obj.addProperty("App::PropertyFloat", "StartY", "Geometry")
        obj.addProperty("App::PropertyFloat", "EndX", "Geometry")
        obj.addProperty("App::PropertyFloat", "EndY", "Geometry")

    def execute(self, obj):
        import FreeCAD
        FreeCAD.Console.PrintMessage(
            f"[STRA_EXECUTE] Executing geometry for node {self.node.node_id}\n"
        )

        node = self.node

        def get_val(name, default=0.0):
            attr = node.attributes.get(name)
            if attr and attr.value:
                try:
                    return float(attr.value)
                except:
                    return default
            return default

        obj.StartX = get_val("StartX", 0.0)
        obj.StartY = get_val("StartY", 0.0)
        obj.EndX = get_val("EndX", 10.0)
        obj.EndY = get_val("EndY", 0.0)

        if hasattr(obj.ViewObject, "Proxy"):
            obj.ViewObject.Proxy.update(obj)
