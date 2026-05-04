import FreeCAD
from PySide import QtWidgets, QtCore

from opetreewb.ui.ope_tree_viewmodel import OPETreeViewModel
from opetreewb.ui.tree_model import TreeNodeModel

from opetreewb.ui.tree_selection_bus import TREE_SELECTION

class OPETreeViewer(QtWidgets.QTreeWidget):
    """
    UI-only OPE Tree Viewer (MVVM).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vm = OPETreeViewModel()

        self.setHeaderHidden(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.itemSelectionChanged.connect(self._on_selection_changed)

        self._build_tree()

    # -------------------------------------------------
    # Tree building
    # -------------------------------------------------
    def _build_tree(self):
        self.clear()
        for root in self.vm.get_roots():
            root_item = self._build_item(root)
            self.addTopLevelItem(root_item)
            root_item.setExpanded(True)

    def _build_item(self, node: TreeNodeModel):
        item = QtWidgets.QTreeWidgetItem([node.label])
        item.setData(0, QtCore.Qt.UserRole, node)

        for child in node.children:
            item.addChild(self._build_item(child))

        return item

    # -------------------------------------------------
    # Selection
    # -------------------------------------------------
    def _on_selection_changed(self):
        items = self.selectedItems()
        if not items:
            return
        
        node = items[0].data(0, QtCore.Qt.UserRole)

        FreeCAD.Console.PrintMessage(
            f"[OPE Tree] Selected node: {node.label}\n"
        )

        self.vm.select_node(node)