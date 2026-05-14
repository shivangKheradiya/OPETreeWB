import FreeCADGui

from opetreewb.ui.selection.selection_observer import OPESelectionObserver


class OPETreeWorkbench(FreeCADGui.Workbench):
    """
    OPETree FreeCAD Workbench (clean rewrite).
    """

    MenuText = "OPE Tree Explorer"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        self._register_ope_commands()
        self._setup_ope_ui()
        FreeCADGui.Selection.addObserver(OPESelectionObserver())

    def _register_ope_commands(self):
        from opetreewb.commands.open_connection_command import \
            OpenConnectionCommand

        FreeCADGui.addCommand(
            "OpenOPEConnection",
            OpenConnectionCommand(),
        )

        from opetreewb.commands.session_commands import (AbortSessionCommand,
                                                         CommitSessionCommand)

        FreeCADGui.addCommand(
            "CommitOPESession",
            CommitSessionCommand(),
        )

        FreeCADGui.addCommand(
            "AbortOPESession",
            AbortSessionCommand(),
        )

        from opetreewb.commands.open_ope_tree_command import OpenOPETreeCommand

        FreeCADGui.addCommand(
            "OpenOPETreeCommand",
            OpenOPETreeCommand(),
        )

        from opetreewb.commands.open_attribute_browser_command import \
            OpenAttributeBrowserCommand

        FreeCADGui.addCommand(
            "OpenOPEAttributeBrowser",
            OpenAttributeBrowserCommand(),
        )

        from opetreewb.commands.open_test_runner_command import \
            OpenTestRunnerCommand

        FreeCADGui.addCommand(
            "OpenOPETestRunner",
            OpenTestRunnerCommand(),
        )

        from opetreewb.commands.sync_commands import (SyncHistoryCommand,
                                                      SyncSnapshotCommand)

        FreeCADGui.addCommand(
            "SyncOPESnapshot",
            SyncSnapshotCommand(),
        )

        FreeCADGui.addCommand(
            "SyncOPEHistory",
            SyncHistoryCommand(),
        )

        from opetreewb.commands.open_3d_space_command import Open3DSpaceCommand

        FreeCADGui.addCommand(
            "OpenOPE3DSpace",
            Open3DSpaceCommand(),
        )

    def _setup_ope_ui(self):
        self.appendMenu(
            "OPE",
            ["OpenOPEConnection"],
        )

        self.appendToolbar(
            "OPE",
            ["OpenOPEConnection"],
        )

        self.appendMenu(
            "OPE_Viewers",
            [
                "OpenOPETreeCommand",
                "OpenOPEAttributeBrowser",
            ],
        )

        self.appendToolbar(
            "OPE_Viewers",
            [
                "OpenOPETreeCommand",
                "OpenOPEAttributeBrowser",
            ],
        )

        self.appendMenu(
            "OPE Session",
            [
                "CommitOPESession",
                "AbortOPESession",
            ],
        )

        self.appendToolbar(
            "OPE Session",
            [
                "CommitOPESession",
                "AbortOPESession",
            ],
        )

        self.appendMenu(
            "OPE Sync",
            [
                "SyncOPESnapshot",
                "SyncOPEHistory",
            ],
        )

        self.appendToolbar(
            "OPE Sync",
            [
                "SyncOPESnapshot",
                "SyncOPEHistory",
            ],
        )

        self.appendMenu(
            "OPE_3D",
            ["OpenOPE3DSpace"],
        )

        self.appendToolbar(
            "OPE_3D",
            ["OpenOPE3DSpace"],
        )

        self.appendMenu(
            "OPE_Developer",
            ["OpenOPETestRunner"],
        )

        self.appendToolbar(
            "OPE_Developer",
            ["OpenOPETestRunner"],
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass
