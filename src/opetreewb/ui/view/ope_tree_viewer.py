import FreeCAD
from PySide import QtWidgets, QtCore

from opetreewb.ui.viewmodels.ope_tree_viewmodel import OPETreeViewModel
from opetreewb.ui.model.tree_model import TreeNodeModel
from opetreewb.ui.tree_label_utils import build_node_label
from opetreewb.domain import CN

class OPETreeViewer(QtWidgets.QTreeWidget):
    """
    UI-only OPE Tree Viewer (MVVM).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vm = OPETreeViewModel()

        self.setHeaderHidden(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._open_context_menu)

        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.itemExpanded.connect(self._on_item_expanded)

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
        label = build_node_label(node)

        item = QtWidgets.QTreeWidgetItem([label])
        item.setData(0, QtCore.Qt.UserRole, node)
        
        item.setChildIndicatorPolicy(
            QtWidgets.QTreeWidgetItem.ShowIndicator
        )

        # No Need To Load All children now
        # for child in node.children:
        #     item.addChild(self._build_item(child))

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
        CN.set(node)

    def _on_item_expanded(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if node is None:
            return
    
        FreeCAD.Console.PrintMessage(
            f"[OPE Tree] Expanding node {node.label}\n"
        )
    
        self.vm.load_children(node)
        
        # ✅ IMPORTANT: clear existing UI children to prevent duplicates
        item.takeChildren()

        # Populate children into UI
        for child in node.children:
            child_item = self._build_item(child)
            item.addChild(child_item)

    def _open_context_menu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return

        menu = QtWidgets.QMenu(self)

        create_action = menu.addAction("Create Child Node")
        delete_action = menu.addAction("Delete Node")

        action = menu.exec_(self.viewport().mapToGlobal(pos))
        if action == create_action:
            self._create_child_node(item)
        
        elif action == delete_action:
            self._delete_node(item)


    def _create_child_node(self, parent_item):
        parent_node = parent_item.data(0, QtCore.Qt.UserRole)
        if parent_node is None:
            return

        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Create Node")

        layout = QtWidgets.QFormLayout(dlg)

        type_edit = QtWidgets.QLineEdit()
        name_edit = QtWidgets.QLineEdit()

        layout.addRow("Element Type:", type_edit)
        layout.addRow("Name (optional):", name_edit)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        layout.addRow(buttons)

        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)

        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return

        element_type = type_edit.text().strip().upper()
        name = name_edit.text().strip()

        if not element_type:
            QtWidgets.QMessageBox.critical(
                self,
                "Invalid Type",
                "Element Type is required",
            )
            return

        # ✅ Delegate model mutation to ViewModel
        new_node = self.vm.create_child_node(
            parent_node,
            element_type,
            name,
        )

        # ✅ UI update only
        child_item = self._build_item(new_node)
        parent_item.addChild(child_item)
        parent_item.setExpanded(True)

        self.setCurrentItem(child_item)

        FreeCAD.Console.PrintMessage(
            f"✅ Created node: {element_type} {name or new_node.node_id}\n"
        )

    def _delete_node(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if node is None:
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Delete Node",
            f"Delete node '{item.text(0)}' and all its children?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        parent_item = item.parent()
        parent_node = (
            parent_item.data(0, QtCore.Qt.UserRole)
            if parent_item else None
        )

        # ✅ Delegate model mutation to ViewModel
        self.vm.delete_node(parent_node, node)

        # ✅ UI update only
        if parent_item:
            parent_item.removeChild(item)
            self.setCurrentItem(parent_item)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)

        FreeCAD.Console.PrintMessage(
            f"✅ Deleted node: {item.text(0)}\n"
        )