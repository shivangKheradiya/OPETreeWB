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
from OPETreeWB.adapters.pydbml_adapter import PyDBMLTreeAdapter
from PyDBML import ElementRef
from OPETreeWB.core.domain_rules import DOMAIN_RULES
from OPETreeWB.core.app_context import APP_CONTEXT

class OPETree(QtWidgets.QTreeWidget):
    """
    Base class for all OPE Trees (DESI, CATA, ENGG, etc).
    """

    def __init__(self, provider, parent=None):
        """
        provider:
            PyDBML provider instance (e.g. OpeApiProvider)
        """

        super().__init__(parent)
        
        self.provider = provider
        self.adapter = PyDBMLTreeAdapter(provider)

        CN.attributeChanged.connect(self._on_attribute_changed)

        self.setHeaderHidden(True)
        self.setSelectionMode(QtWidgets.QTreeWidget.SingleSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.customContextMenuRequested.connect(self._open_context_menu)

        CN.root_node_added.connect(self._on_root_node_added)

        self._build_tree()

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
            

    def _on_root_node_added(self):
        """
        Rebuild tree when nodes are added / deleted.
        """
        self.clear_tree()
        self._add_new_root_node()

    # ---------------------------------------------------------
    # Tree construction
    # ---------------------------------------------------------
    def _build_tree(self):
        self.clear_tree()
        roots = self._discover_world_roots()

        for root_ref in roots:
            root_item = self._build_item_recursive(root_ref)
            self.addTopLevelItem(root_item)
            root_item.setExpanded(True)


    def _build_item_recursive(self, element_ref):
        """
        Build a tree item recursively from an ElementRef.
        """
        label = self.adapter.get_label(element_ref)
        item = self.create_item(label, element_ref)

        for child_ref in self.adapter.get_children(element_ref):
            if child_ref is None:
                continue
            child_item = self._build_item_recursive(child_ref)
            item.addChild(child_item)

        return item
    
    def _discover_world_roots(self):
        """
        Discover WORLD root nodes.
        Criteria:
        - Type == "WORLD"
        - No Owner or Owner is null/0
        """
        domain = APP_CONTEXT.domain
        rules = DOMAIN_RULES.get(domain)
        root_type = rules["RootType"]

        provider = self.provider
        registry = provider.registry

        type_attr = registry.get_id("Type")
        owner_attr = registry.get_id("Owner")

        # 1️⃣ Find all WORLD-typed nodes
        world_rows = provider.search_by_attribute(
            attribute_id=type_attr,
            value=root_type,
        )

        world_node_ids = {row["node_id"] for row in world_rows}

        if not world_node_ids:
            return []

        # 2️⃣ Find nodes that HAVE an Owner
        owner_rows = provider.search_by_attribute(
            attribute_id=owner_attr,
            value=None,  # we only want presence check, value filtered below
        )

        owned_nodes = {
            row["node_id"]
            for row in owner_rows
            if row["value"] not in (None, 0)
        }

        # 3️⃣ Roots = WORLD nodes WITHOUT owner
        root_ids = world_node_ids - owned_nodes

        return [ElementRef(provider, nid) for nid in root_ids]
    

    # ---------------------------------------------------------
    # Hooks (MANDATORY for subclasses)
    # ---------------------------------------------------------
    def get_root_nodes(self):
        raise NotImplementedError