# trees/ope_tree_base.py
"""
Base OPETree implementation.

Responsibilities:
- Display hierarchical nodes
- Hold ElementRef per tree item
- Push selection into global CN

This class is domain-agnostic.
"""

from PySide import QtCore, QtWidgets

from OPETreeWB.core.cn_manager import CN


class OPETree(QtWidgets.QTreeWidget):
    """
    Base class for all OPE Trees (DESI, CATA, ENGG, etc).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        CN.attributeChanged.connect(self._on_attribute_changed)

        self.setHeaderHidden(True)
        self.setSelectionMode(QtWidgets.QTreeWidget.SingleSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.customContextMenuRequested.connect(self._open_context_menu)

        CN.structureChanged.connect(self._on_structure_changed)

    # ---------------------------------------------------------
    # Tree item helpers
    # ---------------------------------------------------------
    def create_item(self, text: str, element_ref=None):
        item = QtWidgets.QTreeWidgetItem([text])
        item.setData(0, QtCore.Qt.UserRole, element_ref)
        return item

    def get_element_ref(self, item):
        return item.data(0, QtCore.Qt.UserRole)

    # -------------------------------------------------
    # Context Menu
    # -------------------------------------------------
    def _open_context_menu(self, pos):
        item = self.itemAt(pos)
        menu = QtWidgets.QMenu(self)

        create_action = menu.addAction("Create Child Node")
        delete_action = None

        if item is not None:
            delete_action = menu.addAction("Delete Node")

        action = menu.exec_(self.viewport().mapToGlobal(pos))
        if action is None:
            return

        if action == create_action:
            self._create_child(item)

        elif delete_action and action == delete_action:
            self._delete_node(item)

    # ---------------------------------------------------------
    # Selection handling
    # ---------------------------------------------------------
    def _on_selection_changed(self):
        items = self.selectedItems()
        CN(items[0].data(0, QtCore.Qt.UserRole) if items else None)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------
    def clear_tree(self):
        """
        Clear all items from the tree.
        """
        self.clear()

    # -------------------------------------------------
    # Create Node
    # -------------------------------------------------
    def _create_child(self, parent_item):
        parent_ref = (
            parent_item.data(0, QtCore.Qt.UserRole)
            if parent_item else None
        )

        provider = parent_ref._provider if parent_ref else None
        if provider is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Create Node",
                "No active provider / parent selected",
            )
            return

        # Ask user for type
        type_value, ok = QtWidgets.QInputDialog.getText(
            self,
            "Create Node",
            "Enter Type:",
        )
        if not ok or not type_value.strip():
            return

        # Create via provider (Step 1 API)
        child_ref = provider.create_node(
            parent_node_id=parent_ref.id,
            type_value=type_value.strip(),
        )

        # Add to tree UI
        label = f"{type_value} {child_ref.id}"
        child_item = self.create_item(label, child_ref)
        parent_item.addChild(child_item)
        parent_item.setExpanded(True)

    # -------------------------------------------------
    # Delete Node (Cascade)
    # -------------------------------------------------
    def _delete_node(self, item):
        element_ref = item.data(0, QtCore.Qt.UserRole)

        if element_ref is None:
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Delete Node",
            "Delete this node and all its children?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        provider = element_ref._provider
        provider.delete_node(element_ref.id)

        # Remove from UI
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            idx = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(idx)

    def _on_attribute_changed(self, element_ref, attr_name):
        """
        If Name changes, update tree label immediately.
        """
        if attr_name != "Name":
            return
    
        root = self.invisibleRootItem()
    
        def find_item(item):
            ref = item.data(0, QtCore.Qt.UserRole)
            if ref is element_ref:
                return item
    
            for i in range(item.childCount()):
                found = find_item(item.child(i))
                if found:
                    return found
            return None
    
        for i in range(root.childCount()):
            item = find_item(root.child(i))
            if item:
                # ✅ Recompute label lazily
                new_label = self.adapter.get_label(element_ref)
                item.setText(0, new_label)
                return
            

    def _on_structure_changed(self):
        """
        Rebuild tree when nodes are added / deleted.
        """
        self.clear_tree()
        self._build_tree()