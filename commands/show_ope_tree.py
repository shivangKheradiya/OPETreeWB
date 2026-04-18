# commands/show_ope_tree.py
"""
Show OPE Tree Explorer command.

This command opens the OPE Tree Explorer as a standalone dockable panel.
It selects between a real PyDBML-backed tree and a mock tree.
"""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtWidgets

from OPETreeWB.core.app_context import APP_CONTEXT
from OPETreeWB.core.provider_factory import create_provider
from OPETreeWB.commands.session_commands import set_active_provider

from OPETreeWB.trees.ope_mock_tree import OPEMockTree
from OPETreeWB.trees.ope_desi_tree import OPEDesiTree


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
        """
        Enable the command only when OPE connection is configured.
        """
        return APP_CONTEXT.is_configured()


    def Activated(self):
        main_window = FreeCADGui.getMainWindow()

        # -------------------------------------------------
        # Avoid creating duplicate dock widgets
        # -------------------------------------------------
        existing = main_window.findChild(
            QtWidgets.QDockWidget, "OPETreeExplorerDock"
        )
        if existing:
            existing.raise_()
            existing.show()
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
        # Choose backend: real provider or mock
        # -------------------------------------------------
        try:
            if not APP_CONTEXT.is_configured():
                raise RuntimeError(
                    "OPE connection or root node is not configured"
                )

            provider = create_provider()
            provider.start_session()

            set_active_provider(provider)

            root_node_id = APP_CONTEXT.root_node_id
            tree = OPEDesiTree(provider, root_node_id, dock)

            FreeCAD.Console.PrintMessage(
                f"OPE Tree: connected to backend "
                f"(root node {root_node_id})\n"
            )

        except Exception as exc:
            FreeCAD.Console.PrintError(
                "OPE Tree: backend unavailable, using mock tree\n"
                f"Reason: {exc}\n"
            )
            tree = OPEMockTree(dock)

        dock.setWidget(tree)

        # -------------------------------------------------
        # Add dock to FreeCAD UI
        # -------------------------------------------------
        main_window.addDockWidget(
            QtCore.Qt.LeftDockWidgetArea,
            dock
        )