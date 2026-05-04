"""
Attribute Viewer (UI-only, MVVM).
"""

import FreeCAD
from PySide.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from PySide.QtCore import Qt

from opetreewb.ui.attribute_viewmodel import AttributeViewerViewModel
from opetreewb.ui.tree_selection_bus import TREE_SELECTION


class AttributeViewer(QWidget):
    """
    Dockable Attribute Viewer.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vm = AttributeViewerViewModel()
        self.vm.data_changed.connect(self._refresh)

        self._building = False
        self._build_ui()

        # Selection bus
        TREE_SELECTION.selectionChanged.connect(
            self.vm._on_node_selected
        )
        
        self.table.itemChanged.connect(self._on_item_changed)
        self.vm.attribute_value_changed.connect(self._on_attribute_value_changed)

    # -------------------------------------------------
    # UI setup
    # -------------------------------------------------
    def _build_ui(self):
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Attribute", "Value", "Data ID"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setEditTriggers(
            QTableWidget.DoubleClicked |
            QTableWidget.EditKeyPressed
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    # -------------------------------------------------
    # Rendering
    # -------------------------------------------------
    def _refresh(self):
        self._building = True
        self.table.blockSignals(True)

        rows = self.vm.get_rows()
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            self._set_item(r, 0, row.attribute, editable=False)
            self._set_item(r, 1, row.value, editable=True)
            self._set_item(r, 2, row.data_id, editable=False)

        FreeCAD.Console.PrintMessage(
            f"[AttributeViewer] Showing {len(rows)} attributes\n"
        )

        self.table.blockSignals(False)
        self._building = False

    def _set_item(self, row, col, text, editable):
        item = QTableWidgetItem(str(text))
        if not editable:
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(row, col, item)

    def _on_item_changed(self, item):
        if self._building:
            return

        # Only Value column (column index 1)
        if item.column() != 1:
            return

        row_index = item.row()
        new_value = item.text()

        self.vm.update_value(row_index, new_value)

    def _on_attribute_value_changed(self, data_id: int, new_value: str):
        FreeCAD.Console.PrintMessage(
            f"[AttributeViewer] Attribute changed: data_id={data_id}, value={new_value}\n"
        )