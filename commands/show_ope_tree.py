# commands/show_ope_tree.py
"""
Command to show the OPE Tree dock panel.
"""

import FreeCADGui

from PySide2.QtWidgets import QDockWidget, QWidget, QSplitter
from PySide2.QtCore import Qt

from OPETreeWB.trees.ope_tree_base import OPETree
from OPETreeWB.ui.attribute_viewer import AttributeViewer
from OPETreeWB.trees.ope_mock_tree import OPEMockTree

class ShowOPETreeCommand:
    """
    FreeCAD command that shows the OPE Tree panel.
    """

    def GetResources(self):
        return {
            "MenuText": "Show OPE Tree",
            "ToolTip": "Open the OPE Tree explorer",
        }

    def IsActive(self):
        return True

    def Activated(self):
        mw = FreeCADGui.getMainWindow()

        # Avoid creating duplicate dock widgets
        existing = mw.findChild(QDockWidget, "OPETreeDock")
        if existing:
            existing.raise_()
            existing.show()
            return

        dock = QDockWidget("OPE Tree", mw)
        dock.setObjectName("OPETreeDock")
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea
        )

        container = QWidget(dock)
        splitter = QSplitter(Qt.Vertical, container)

        # Tree (empty for now, domain trees come later)
        # tree = OPETree(splitter)
        tree = OPEMockTree(splitter)

        # Attribute viewer (CN-driven)
        attr_viewer = AttributeViewer(splitter)

        splitter.addWidget(tree)
        splitter.addWidget(attr_viewer)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        dock.setWidget(container)
        mw.addDockWidget(Qt.RightDockWidgetArea, dock)