import FreeCAD
import FreeCADGui


class Open3DSpaceCommand:
    def GetResources(self):
        return {
            "MenuText": "Open 3D Space",
            "ToolTip": "Open temporary 3D workspace",
        }

    def IsActive(self):
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage(
            "✅ 3D Space opened (temporary stub)\n"
        )

        doc = FreeCAD.newDocument("OPE_3D_TEMP")
        FreeCADGui.ActiveDocument.ActiveView.viewIsometric()
        FreeCADGui.SendMsgToActiveView("ViewFit")