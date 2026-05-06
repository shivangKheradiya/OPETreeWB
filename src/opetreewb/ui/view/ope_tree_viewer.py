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
        # self.itemExpanded.connect(self._on_item_expanded)
     
        CN.structure_changed.connect(self._on_structure_changed)
        CN.deleted.connect(self._on_structure_changed)

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

        # ✅ Recursively add children NOW (no lazy loading)
        for child in node.children:
            child_item = self._build_item(child)
            item.addChild(child_item)

        return item

    # -------------------------------------------------
    # Selection
    # -------------------------------------------------
    def _on_selection_changed(self):

        # ✅ Prevent recursion during tree rebuild
        if self.signalsBlocked():
            return

        items = self.selectedItems()
        if not items:
            return
        
        node = items[0].data(0, QtCore.Qt.UserRole)

        FreeCAD.Console.PrintMessage(
            f"[OPE Tree] Selected node: {node.label}\n"
        )

        CN.set(node)

    def _on_item_expanded(self, item):
        pass
        #node = item.data(0, QtCore.Qt.UserRole)
        #if node is None:
        #    return
        #
        #FreeCAD.Console.PrintMessage(
        #    f"[OPE Tree] Expanding node {node.label}\n"
        #)
        #
        #self.vm.load_children(node)
        #
        ## ✅ IMPORTANT: clear existing UI children to prevent duplicates
        #item.takeChildren()
        #
        ## Populate children into UI
        #for child in node.children:
        #    child_item = self._build_item(child)
        #    item.addChild(child_item)

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

        # Ensure CN context is correct
        CN.set(parent_node)

        # ✅ Create via CN (TX-safe)
        CN.create_child(element_type, name)

        FreeCAD.Console.PrintMessage(
            f"✅ Create node request sent: {element_type} {name}\n"
        )

    def _delete_node(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if node is None:
            return

        lable = item.text(0)

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Delete Node",
            f"Delete node '{lable}' and all its children?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        # ✅ SINGLE source of truth
        CN.set(node)
        CN.delete()

        FreeCAD.Console.PrintMessage(
            f"✅ Delete request sent: {lable}\n"
        )

    def _on_structure_changed(self):
        self._rebuild_tree_preserve_selection()

    def _on_cn_deleted(self, node):
        self._refresh_tree()

    def _rebuild_tree_preserve_selection(self):
        selected_id = CN.node.node_id if CN.node else None

        # Block signals to prevent recursion
        self.blockSignals(True)

        self._build_tree()

        if selected_id is not None:
            item = self._find_item_by_node_id(selected_id)
        if item:
            self.setCurrentItem(item)

        self.blockSignals(False)

    def _find_item_by_node_id(self, node_id):
        def traverse(item):
            if item.data(0, QtCore.Qt.UserRole).node_id == node_id:
                return item
            for i in range(item.childCount()):
                result = traverse(item.child(i))
                if result:
                    return result
            return None

        for i in range(self.topLevelItemCount()):
            result = traverse(self.topLevelItem(i))
            if result:
                return result
        return None
