import json
import math

from pivy import coin


class ViewProviderCirc:
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

        FreeCAD.Console.PrintMessage(f"[CIRC_VIEW] update node={node.node_id}\n")

        cx = obj.CenterX
        cy = obj.CenterY
        r = obj.Radius

        # -------------------------------------------------
        # ✅ GEOMETRY (circle approximation)
        # -------------------------------------------------
        points = []
        segments = 64  # smoothness

        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append(coin.SbVec3f(x, y, 0))

        self.coords.point.setValues(0, len(points), points)
        self.lines.numVertices.set1Value(0, len(points))

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
                    r_val, g_val, b_val = float(val[0]), float(val[1]), float(val[2])

                    # normalize if needed
                    if max(r_val, g_val, b_val) > 1:
                        r_val /= 255.0
                        g_val /= 255.0
                        b_val /= 255.0

                    color = (r_val, g_val, b_val)

            except Exception:
                FreeCAD.Console.PrintWarning(
                    f"[CIRC_VIEW] invalid color: {repr(raw)}\n"
                )

        self.material.diffuseColor.setValue(*color)
