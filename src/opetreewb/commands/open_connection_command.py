"""
FreeCAD command to open the OPE Connection dialog (UI only).
"""

import FreeCADGui

from opetreewb.ui.view.connection_dialog import ConnectionDialog


class OpenConnectionCommand:
    """Open the OPE Connection Setup dialog."""

    def GetResources(self):
        return {
            "MenuText": "OPE Connection",
            "ToolTip": "Open OPE connection setup dialog (UI only)",
        }

    def IsActive(self):
        # Always available (UI only)
        return True

    def Activated(self):
        dialog = ConnectionDialog(parent=FreeCADGui.getMainWindow())
        dialog.exec_()
