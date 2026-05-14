import FreeCADGui

from opetreewb.ui.view.test_runner_dialog import TestRunnerDialog


class OpenTestRunnerCommand:
    def GetResources(self):
        return {
            "MenuText": "Test Runner",
            "ToolTip": "Select and run OPETreeWB tests",
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.dialog = TestRunnerDialog(FreeCADGui.getMainWindow())
        self.dialog.exec_()
