import FreeCADGui


class OPETreeWorkbench(FreeCADGui.Workbench):
    """
    OPETree FreeCAD Workbench (clean rewrite).
    """

    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        # Commands will be registered here step by step
        pass

    def Activated(self):
        pass

    def Deactivated(self):
        pass