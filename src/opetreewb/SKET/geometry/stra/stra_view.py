from pivy import coin


class ViewProviderStra:

    def __init__(self, vobj):

        vobj.Proxy = self

        self.root = coin.SoSeparator()
        vobj.RootNode.addChild(self.root)

        self.material = coin.SoMaterial()
        self.material.diffuseColor.setValue(0, 0, 0)

        self.drawstyle = coin.SoDrawStyle()
        self.drawstyle.lineWidth = 2

        self.coords = coin.SoCoordinate3()
        self.lines = coin.SoLineSet()

        self.root.addChild(self.material)
        self.root.addChild(self.drawstyle)
        self.root.addChild(self.coords)
        self.root.addChild(self.lines)

    def update(self, obj):

        pts = [
            coin.SbVec3f(obj.StartX, obj.StartY, 0),
            coin.SbVec3f(obj.EndX, obj.EndY, 0),
        ]

        self.coords.point.setValues(0, 2, pts)
        self.lines.numVertices.set1Value(0, 2)

    def getDisplayModes(self, vobj):
        return ["Default"]

    def getDefaultDisplayMode(self):
        return "Default"
