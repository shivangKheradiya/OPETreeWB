from pivy import coin
import json


class ViewProviderRect:

    def __init__(self, vobj):
        vobj.Proxy = self

        self.root = coin.SoSeparator()
        vobj.RootNode.addChild(self.root)

        # ✅ style
        self.material = coin.SoMaterial()
        self.drawstyle = coin.SoDrawStyle()

        # ✅ geometry
        self.coords = coin.SoCoordinate3()
        self.lines = coin.SoLineSet()

        self.root.addChild(self.material)
        self.root.addChild(self.drawstyle)
        self.root.addChild(self.coords)
        self.root.addChild(self.lines)

    def update(self, obj):

        import FreeCAD

        node = getattr(obj.Proxy, "node", None)
        if not node:
            return

        attrs = node.attributes

        FreeCAD.Console.PrintMessage(
            f"[RECT_VIEW] updating node={node.node_id}\n"
        )

        x = obj.X
        y = obj.Y
        w = obj.Width
        h = obj.Height

        # -------------------------------------------------
        # ✅ RECTANGLE GEOMETRY
        # -------------------------------------------------
        pts = [
            coin.SbVec3f(x, y, 0),
            coin.SbVec3f(x + w, y, 0),
            coin.SbVec3f(x + w, y + h, 0),
            coin.SbVec3f(x, y + h, 0),
            coin.SbVec3f(x, y, 0),  # close shape
        ]

        self.coords.point.setValues(0, len(pts), pts)
        self.lines.numVertices.set1Value(0, len(pts))

        # -------------------------------------------------
        # ✅ STYLE (pattern)
        # -------------------------------------------------
        style_attr = attrs.get("LineStyle")
        style = style_attr.value if style_attr and style_attr.value else "Solid"

        if style == "Dashed":
            self.drawstyle.linePattern = 0x00FF
        elif style == "Dotted":
            self.drawstyle.linePattern = 0x0101
        elif style == "DashDot":
            self.drawstyle.linePattern = 0x1C47
        else:
            self.drawstyle.linePattern = 0xFFFF

        # -------------------------------------------------
        # ✅ WIDTH
        # -------------------------------------------------
        width_attr = attrs.get("LineWidth")

        try:
            width = float(width_attr.value) if width_attr and width_attr.value else 2.0
        except Exception:
            width = 2.0

        self.drawstyle.lineWidth = width

        # -------------------------------------------------
        # ✅ COLOR
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
                    f"[RECT_VIEW] invalid color: {repr(raw)}\n"
                )

        self.material.diffuseColor.setValue(*color)
