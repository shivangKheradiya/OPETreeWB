import FreeCAD
import FreeCADGui


class RunOPETestsCommand:
    """
    FreeCAD command to run all OPETreeWB tests.
    """

    def GetResources(self):
        return {
            "MenuText": "Run OPE Tests",
            "ToolTip": "Run all OPETreeWB tests and print results to console",
        }

    def IsActive(self):
        # Always available
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage(
            "\n[OPETreeWB] Running tests...\n"
        )

        try:
            from opetreewb.tests.run_tests import run_all
            run_all()
        except Exception as exc:
            import traceback
            FreeCAD.Console.PrintError(
                "[OPETreeWB] Test execution failed\n"
            )
            traceback.print_exc()