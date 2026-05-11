import FreeCAD
from PySide import QtWidgets, QtCore

from opetreewb.ui.viewmodels.ope_tree_viewmodel import OPETreeViewModel
from opetreewb.ui.model.tree_model import TreeNodeModel
from opetreewb.ui.tree_label_utils import build_node_label
from opetreewb.domain import CN
from opetreewb.domain.services.service_locator import (
    get_geometry_service,
)


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
     
        CN.structure_changed.connect(self._on_structure_changed)
        CN.deleted.connect(self._on_structure_changed)

        self._build_tree()

    # -------------------------------------------------
    # Tree building
    # -------------------------------------------------
    def _build_tree(self):
        self.clear()
        roots = self.vm.get_roots()
        if not roots:
            FreeCAD.Console.PrintMessage("[Tree] No roots found\n")
            return

        for root in roots:
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
        
        menu.addSeparator()
        
        addCN_action = menu.addAction("Add CN")
        remCN_action = menu.addAction("Rem CN")

        action = menu.exec_(self.viewport().mapToGlobal(pos))
        if action == create_action:
            self._create_child_node(item)
        
        elif action == delete_action:
            self._delete_node(item)

        elif action == addCN_action:
            self._addIn3D_node(item)

        elif action == remCN_action:
            self._remFrom3D_node(item)

    def _create_child_node(self, parent_item):
        parent_node = parent_item.data(0, QtCore.Qt.UserRole)
        if parent_node is None:
            return

        CN.set(parent_node)
        
        allowed_types = CN.allowed_child_types()
        if not allowed_types:
            QtWidgets.QMessageBox.information(
                self,
                "Not Allowed",
                "This element cannot have children."
            )
            return
        
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Create Node")

        layout = QtWidgets.QFormLayout(dlg)

        type_combo = QtWidgets.QComboBox()
        name_edit = QtWidgets.QLineEdit()

        type_combo.addItems(allowed_types)

        layout.addRow("Element Type:", type_combo)
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

        element_type = type_combo.currentText()
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
        node_id = CN.create_child(element_type, name)

        # new_node = CN._node
        # parent_node.children.append(new_node)
        # 
        # child_item = self._build_item(new_node)
        # parent_item.addChild(child_item)

        # expand parent (very important)
        parent_item.setExpanded(True)

        FreeCAD.Console.PrintMessage(
            f"✅ Create node request sent: {element_type} {name}\n"
        )

    def _delete_node(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if node is None:
            return
        
        parent_item = item.parent()

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

        if parent_item:
            parent_item.removeChild(item)
            self.setCurrentItem(parent_item)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)

        FreeCAD.Console.PrintMessage(
            f"✅ Delete request sent: {lable}\n"
        )

    def _on_structure_changed(self):
        pass

    def _addIn3D_node(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if not node:
            return

        from opetreewb.domain import CN
        CN.set(node)

        # ✅ Build geometry
        get_geometry_service().build(CN.node)

        FreeCAD.Console.PrintMessage(
            f"✅ Geometry built for: {node.label}\n"
        )

    def _remFrom3D_node(self, item):
        node = item.data(0, QtCore.Qt.UserRole)
        if not node:
            return

        from opetreewb.domain import CN
        CN.set(node)

        # ✅ Remove geometry
        get_geometry_service().remove(CN.node)

        FreeCAD.Console.PrintMessage(
            f"✅ Geometry removed for: {node.label}\n"
        )
