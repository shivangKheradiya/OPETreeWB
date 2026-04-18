# trees/ope_tree_base.py
"""
Base OPETree implementation.

Responsibilities:
- Display hierarchical nodes
- Hold ElementRef per tree item
- Push selection into global CN

This class is domain-agnostic.
"""

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Qt

from OPETreeWB.core.cn_manager import CN


class OPETree(QTreeWidget):
    """
    Base class for all OPE Trees (DESI, CATA, ENGG, etc).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setHeaderHidden(True)
        self.setSelectionMode(QTreeWidget.SingleSelection)

        # Selection handling
        self.itemSelectionChanged.connect(self._on_selection_changed)

    # ---------------------------------------------------------
    # Tree item helpers
    # ---------------------------------------------------------
    def create_item(self, text: str, element_ref=None) -> QTreeWidgetItem:
        """
        Create a tree item and attach an ElementRef to it.
        """
        item = QTreeWidgetItem([text])
        item.setData(0, Qt.UserRole, element_ref)
        return item

    def get_element_ref(self, item: QTreeWidgetItem):
        """
        Retrieve ElementRef stored on a tree item.
        """
        return item.data(0, Qt.UserRole)

    # ---------------------------------------------------------
    # Selection handling
    # ---------------------------------------------------------
    def _on_selection_changed(self):
        items = self.selectedItems()
        if not items:
            CN(None)
            return

        item = items[0]
        element_ref = self.get_element_ref(item)

        # Push into global CN
        CN(element_ref)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------
    def clear_tree(self):
        """
        Clear all items from the tree.
        """
        self.clear()