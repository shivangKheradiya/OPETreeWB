import json

from pivy import coin


class ViewProviderTexp:
    def __init__(self, vobj):
        vobj.Proxy = self

        self.root = coin.SoSeparator()
        vobj.RootNode.addChild(self.root)

        # ✅ positioning+scale
        self.transform = coin.SoTransform()

        # ✅ style
        self.material = coin.SoMaterial()
        self.font = coin.SoFont()

        # ✅ text node
        self.text = coin.SoText3()

        # ✅ assemble graph
        self.root.addChild(self.transform)
        self.root.addChild(self.material)
        self.root.addChild(self.font)
        self.root.addChild(self.text)

    def update(self, obj):

        import FreeCAD

        node = getattr(obj.Proxy, "node", None)
        if not node:
            return

        attrs = node.attributes

        FreeCAD.Console.PrintMessage(f"[TEXT_VIEW] updating node={node.node_id}\n")

        # -------------------------------------------------
        # ✅ POSITION
        # -------------------------------------------------
        self.transform.translation.setValue(obj.X, obj.Y, 0)

        # -------------------------------------------------
        # ✅ TEXT CONTENT
        # -------------------------------------------------
        self.text.string.setValue(obj.Text)

        # -------------------------------------------------
        # ✅ FONT SIZE
        # -------------------------------------------------
        size = obj.FontSize if obj.FontSize else 12
        scale_factor = size * 0.1

        self.transform.scaleFactor.setValue(scale_factor, scale_factor, scale_factor)

        # -------------------------------------------------
        # ✅ COLOR (same parser as STRA)
        # -------------------------------------------------
        color_attr = attrs.get("LineColor")

        color = (0.0, 0.0, 0.0)

        if color_attr and color_attr.value:
            raw = color_attr.value

            try:
                val = raw

                if isinstance(val, str):
                    val = json.loads(val)

                if isinstance(val, (list, tuple)) and len(val) == 3:
                    r, g, b = float(val[0]), float(val[1]), float(val[2])

                    if max(r, g, b) > 1:
                        r /= 255.0
                        g /= 255.0
                        b /= 255.0

                    color = (r, g, b)

            except Exception:
                FreeCAD.Console.PrintWarning(
                    f"[TEXT_VIEW] invalid color: {repr(raw)}\n"
                )

        self.material.diffuseColor.setValue(*color)
