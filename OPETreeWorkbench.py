# OPETreeWorkbench.py

import FreeCADGui

class OPETreeWorkbench(FreeCADGui.Workbench):
    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        from OPETreeWB.commands.show_ope_tree import ShowOPETreeCommand
        from OPETreeWB.commands.show_attribute_browser import ShowAttributeBrowserCommand
        from OPETreeWB.commands.session_commands import (
            StartSessionCommand,
            CommitSessionCommand,
            AbortSessionCommand,
        )
        from OPETreeWB.commands.show_connection_ui import ShowConnectionUICommand

        FreeCADGui.addCommand("ShowOPEConnectionUI", ShowConnectionUICommand())
        FreeCADGui.addCommand("StartOPESession", StartSessionCommand())
        FreeCADGui.addCommand("CommitOPESession", CommitSessionCommand())
        FreeCADGui.addCommand("AbortOPESession", AbortSessionCommand())

        self.appendMenu(
            "OPE Session",
            [
                "StartOPESession",
                "CommitOPESession",
                "AbortOPESession",
            ]
        )

        self.appendToolbar(
            "OPE Session",
            [
                "StartOPESession",
                "CommitOPESession",
                "AbortOPESession",
            ]
        )

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

        self.appendMenu(
            "OPE",
            ["ShowOPEConnectionUI"]
        )
        
        self.appendToolbar(
            "OPE",
            ["ShowOPEConnectionUI"]
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass