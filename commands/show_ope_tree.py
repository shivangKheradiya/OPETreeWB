# commands/show_ope_tree.py
"""
Command to show the OPE Tree dock panel.
"""

import FreeCADGui

from PySide import QtCore, QtWidgets

from OPETreeWB.ui.attribute_viewer import AttributeViewer

# --- Tree choices ---
from OPETreeWB.trees.ope_mock_tree import OPEMockTree
# from OPETreeWB.trees.ope_desi_tree import OPEDesiTree


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
        existing = mw.findChild(QtWidgets.QDockWidget, "OPETreeDock")
        if existing:
            existing.raise_()
            existing.show()
            return

        dock = QtWidgets.QDockWidget("OPE Tree", mw)
        dock.setObjectName("OPETreeDock")
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea |
            QtCore.Qt.RightDockWidgetArea
        )

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # -------------------------------------------------
        # TREE SELECTION POINT
        # -------------------------------------------------

        # ✅ SAFE DEFAULT (mock data)
        tree = OPEMockTree(splitter)

        # 🔧 REAL DATA (enable later)
        # provider = ...
        # root_node_id = ...
        # tree = OPEDesiTree(provider, root_node_id, splitter)

        attr_viewer = AttributeViewer(splitter)

        splitter.addWidget(tree)
        splitter.addWidget(attr_viewer)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        dock.setWidget(splitter)
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)