# commands/show_connection_ui.py
"""
Command to show the OPE Connection Setup dialog.
"""

import FreeCADGui
from OPETreeWB.ui.connection_dialog import ConnectionDialog


class ShowConnectionUICommand:
    def GetResources(self):
        return {
            "MenuText": "OPE Connection Setup",
            "ToolTip": "Configure API and project connection",
        }

    def IsActive(self):
        return True

    def Activated(self):
        main_window = FreeCADGui.getMainWindow()
        dialog = ConnectionDialog(main_window)
        dialog.exec_()