# commands/show_attribute_browser.py
"""
Show OPE Attribute Browser command.

This command opens the Attribute Browser as a standalone dockable panel.
It listens to the global Current Node (CN) and updates automatically.
"""

import FreeCADGui
from PySide import QtCore, QtWidgets

from OPETreeWB.ui.attribute_viewer import AttributeViewer


class ShowAttributeBrowserCommand:
    """
    FreeCAD command to show the OPE Attribute Browser panel.
    """

    def GetResources(self):
        return {
            "MenuText": "Show OPE Attribute Browser",
            "ToolTip": "Open the OPE Attribute Browser",
        }

    def IsActive(self):
        # Always available
        return True

    def Activated(self):
        """
        Called when the user clicks the command.
        """
        main_window = FreeCADGui.getMainWindow()

        # -------------------------------------------------
        # Avoid creating duplicate dock widgets
        # -------------------------------------------------
        existing_dock = main_window.findChild(
            QtWidgets.QDockWidget, "OPEAttributeBrowserDock"
        )
        if existing_dock:
            existing_dock.raise_()
            existing_dock.show()
            return

        # -------------------------------------------------
        # Create dock widget
        # -------------------------------------------------
        dock = QtWidgets.QDockWidget("OPE Attribute Browser", main_window)
        dock.setObjectName("OPEAttributeBrowserDock")

        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea |
            QtCore.Qt.RightDockWidgetArea |
            QtCore.Qt.BottomDockWidgetArea
        )

        # -------------------------------------------------
        # Create attribute viewer (ONLY this widget)
        # -------------------------------------------------
        attr_viewer = AttributeViewer(dock)

        dock.setWidget(attr_viewer)

        # -------------------------------------------------
        # Add dock to FreeCAD UI
        # -------------------------------------------------
        main_window.addDockWidget(
            QtCore.Qt.RightDockWidgetArea,
            dock
        )