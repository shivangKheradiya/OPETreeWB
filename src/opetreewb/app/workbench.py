import FreeCADGui


class OPETreeWorkbench(FreeCADGui.Workbench):
    """
    OPETree FreeCAD Workbench (clean rewrite).
    """

    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        self._register_commands()
        self._setup_ui()

    def _register_commands(self):
        from opetreewb.commands.open_connection_command import (
            OpenConnectionCommand,
        )

        FreeCADGui.addCommand(
            "OpenOPEConnection",
            OpenConnectionCommand(),
        )

        from opetreewb.commands.open_test_runner_command import (
            OpenTestRunnerCommand,
        )

        FreeCADGui.addCommand(
            "OpenOPETestRunner",
            OpenTestRunnerCommand(),
        )

    def _setup_ui(self):
        self.appendMenu(
            "OPE",
            ["OpenOPEConnection"],
        )

        self.appendToolbar(
            "OPE",
            ["OpenOPEConnection"],
        )        
        
        self.appendMenu(
            "OPE Developer",
            ["OpenOPETestRunner"],
        )

        self.appendToolbar(
            "OPE Developer",
            ["OpenOPETestRunner"],
        )

    def Activated(self):
        pass

    def Deactivated(self):
        pass