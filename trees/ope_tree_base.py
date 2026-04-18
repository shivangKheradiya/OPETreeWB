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

        self.setHeaderHidden(True)
        self.setSelectionMode(QtWidgets.QTreeWidget.SingleSelection)

        self.itemSelectionChanged.connect(self._on_selection_changed)

    # ---------------------------------------------------------
    # Tree item helpers
    # ---------------------------------------------------------
    def create_item(self, text: str, element_ref=None):
        item = QtWidgets.QTreeWidgetItem([text])
        item.setData(0, QtCore.Qt.UserRole, element_ref)
        return item

    def get_element_ref(self, item):
        return item.data(0, QtCore.Qt.UserRole)

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