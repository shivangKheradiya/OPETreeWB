import FreeCADGui
from PySide.QtCore import Qt
from PySide.QtWidgets import QDockWidget

from opetreewb.ui.view.ope_tree_viewer import OPETreeViewer


class OpenOPETreeCommand:
    DOCK_NAME = "OPETreeDock"

    def GetResources(self):
        return {
            "MenuText": "OPE Tree Explorer",
            "ToolTip": "Open OPE Tree Viewer",
        }

    def IsActive(self):
        return True

    def Activated(self):
        mw = FreeCADGui.getMainWindow()

        for dock in mw.findChildren(QDockWidget):
            if dock.objectName() == self.DOCK_NAME:
                dock.raise_()
                dock.show()
                return

        viewer = OPETreeViewer(mw)
        dock = QDockWidget("OPE Tree", mw)
        dock.setObjectName(self.DOCK_NAME)
        dock.setWidget(viewer)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        mw.addDockWidget(Qt.LeftDockWidgetArea, dock)
        dock.show()
