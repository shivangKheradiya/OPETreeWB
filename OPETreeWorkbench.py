# OPETreeWorkbench.py

import FreeCADGui

class OPETreeWorkbench(FreeCADGui.Workbench):
    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        from OPETreeWB.commands.show_ope_tree import ShowOPETreeCommand

        FreeCADGui.addCommand(
            "ShowOPETree",
            ShowOPETreeCommand()
        )

        self.appendMenu(
            "OPE Tree",
            ["ShowOPETree"]
        )

        self.appendToolbar(
            "OPE Tree",
            ["ShowOPETree"]
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass