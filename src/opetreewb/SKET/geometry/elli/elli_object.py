class ElliObject:

    def __init__(self, obj, node):

        obj.Proxy = self
        self.node = node
        obj.Proxy.node = node

        obj.addProperty("App::PropertyFloat", "CenterX", "Geometry")
        obj.addProperty("App::PropertyFloat", "CenterY", "Geometry")
        obj.addProperty("App::PropertyFloat", "MajorRadius", "Geometry")
        obj.addProperty("App::PropertyFloat", "MinorRadius", "Geometry")

    def execute(self, obj):

        node = self.node

        def get_val(name, default):
            attr = node.attributes.get(name)
            if attr and attr.value is not None:
                return float(attr.value)
            return default

        obj.CenterX = get_val("CenterX", 0)
        obj.CenterY = get_val("CenterY", 0)
        obj.MajorRadius = get_val("MajorRadius", 5)
        obj.MinorRadius = get_val("MinorRadius", 3)

        obj.ViewObject.Proxy.update(obj)