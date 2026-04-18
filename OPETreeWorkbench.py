# OPETreeWorkbench.py

import FreeCADGui

class OPETreeWorkbench(FreeCADGui.Workbench):
    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        from OPETreeWB.commands.show_ope_tree import ShowOPETreeCommand
        from OPETreeWB.commands.show_attribute_browser import ShowAttributeBrowserCommand

        FreeCADGui.addCommand(
            "ShowOPETree",
            ShowOPETreeCommand()
        )

        FreeCADGui.addCommand(
            "ShowOPEAttributeBrowser",
            ShowAttributeBrowserCommand()
        )

        self.appendMenu(
            "OPE Tree",
            [
                "ShowOPETree",
                "ShowOPEAttributeBrowser",
            ]
        )

        self.appendToolbar(
            "OPE Tree",
            [
                "ShowOPETree",
                "ShowOPEAttributeBrowser",
            ]
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass