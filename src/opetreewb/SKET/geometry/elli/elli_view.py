from pivy import coin
import math


class ViewProviderElli:

    def __init__(self, vobj):
        vobj.Proxy = self

        self.root = coin.SoSeparator()
        vobj.RootNode.addChild(self.root)

        self.material = coin.SoMaterial()
        self.drawstyle = coin.SoDrawStyle()
        self.coords = coin.SoCoordinate3()
        self.lines = coin.SoLineSet()

        self.root.addChild(self.material)
        self.root.addChild(self.drawstyle)
        self.root.addChild(self.coords)
        self.root.addChild(self.lines)

    def update(self, obj):

        cx = obj.CenterX
        cy = obj.CenterY
        a = obj.MajorRadius
        b = obj.MinorRadius

        pts = []

        segments = 64

        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = cx + a * math.cos(angle)
            y = cy + b * math.sin(angle)
            pts.append(coin.SbVec3f(x, y, 0))

        self.coords.point.setValues(0, len(pts), pts)
        self.lines.numVertices.set1Value(0, len(pts))
