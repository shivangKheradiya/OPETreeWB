# commands/show_ope_tree.py
"""
Show OPE Tree Explorer command.

This command opens the OPE Tree Explorer as a standalone dockable panel.
It does NOT create or manage the Attribute Browser.
"""

import FreeCADGui
from PySide import QtCore, QtWidgets

# Import the tree you want to show
# For now we use the mock tree
from OPETreeWB.trees.ope_mock_tree import OPEMockTree
# Later you can switch to:
# from OPETreeWB.trees.ope_desi_tree import OPEDesiTree
# from OPETreeWB.commands.session_commands import set_active_provide

class ShowOPETreeCommand:
    """
    FreeCAD command to show the OPE Tree Explorer panel.
    """

    def GetResources(self):
        return {
            "MenuText": "Show OPE Tree Explorer",
            "ToolTip": "Open the OPE Tree Explorer",
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
            QtWidgets.QDockWidget, "OPETreeExplorerDock"
        )
        if existing_dock:
            existing_dock.raise_()
            existing_dock.show()
            return

        # -------------------------------------------------
        # Create dock widget
        # -------------------------------------------------
        dock = QtWidgets.QDockWidget("OPE Tree Explorer", main_window)
        dock.setObjectName("OPETreeExplorerDock")

        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea |
            QtCore.Qt.RightDockWidgetArea
        )

        # -------------------------------------------------
        # Create tree widget (ONLY the tree)
        # -------------------------------------------------
        tree = OPEMockTree(dock)

        # Example for real data later:
        # provider = ...
        # root_node_id = ...
        # tree = OPEDesiTree(provider, root_node_id, dock)
        
        # provider = create_desi_provider()   # <-- your code
        # root_node_id = 1001
        # set_active_provider(provider)

        dock.setWidget(tree)

        # -------------------------------------------------
        # Add dock to FreeCAD UI
        # -------------------------------------------------
        main_window.addDockWidget(
            QtCore.Qt.LeftDockWidgetArea,
            dock
        )