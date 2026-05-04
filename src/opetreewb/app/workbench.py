import FreeCADGui


class OPETreeWorkbench(FreeCADGui.Workbench):
    """
    OPETree FreeCAD Workbench (clean rewrite).
    """

    MenuText = "OPE Tree"
    ToolTip = "OPE Tree Explorer for DBML-based domains"

    def Initialize(self):
        from opetreewb.commands.run_tests_command import RunOPETestsCommand

        FreeCADGui.addCommand(
            "RunOPETests",
            RunOPETestsCommand()
        )

        self.appendMenu(
            "OPE Developer",
            ["RunOPETests"]
        )

        self.appendToolbar(
            "OPE Developer",
            ["RunOPETests"]
        )

        from opetreewb.commands.open_test_runner_command import (
            OpenTestRunnerCommand,
        )

        FreeCADGui.addCommand(
            "OpenOPETestRunner",
            OpenTestRunnerCommand(),
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