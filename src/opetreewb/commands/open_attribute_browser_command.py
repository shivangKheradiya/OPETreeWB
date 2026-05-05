"""
FreeCAD command to open the Attribute Viewer (UI only).
"""

import FreeCADGui
from PySide.QtWidgets import QDockWidget
from PySide.QtCore import Qt

from opetreewb.ui.view.attribute_viewer import AttributeViewer


class OpenAttributeBrowserCommand:
    """Open the OPE Attribute Browser (UI only)."""

    DOCK_NAME = "OPEAttributeBrowserDock"
    
    def GetResources(self):
        return {
            "MenuText": "OPE Attribute Browser",
            "ToolTip": "Open OPE Attribute Browser (UI only)",
        }

    def IsActive(self):
        # Always available for UI testing
        return True

    def Activated(self):
        main_window = FreeCADGui.getMainWindow()

        # -------------------------------------------------
        # Avoid creating multiple dock widgets
        # -------------------------------------------------
        for dock in main_window.findChildren(QDockWidget):
            if dock.objectName() == self.DOCK_NAME:
                dock.raise_()
                dock.show()
                return

        # -------------------------------------------------
        # Create dock widget
        # -------------------------------------------------
        viewer = AttributeViewer(parent=main_window)

        dock = QDockWidget("OPE Attribute Browser", main_window)
        dock.setObjectName(self.DOCK_NAME)
        dock.setWidget(viewer)

        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea |
            Qt.BottomDockWidgetArea
        )

        # -------------------------------------------------
        # Add to FreeCAD main window
        # -------------------------------------------------
        main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.show()
