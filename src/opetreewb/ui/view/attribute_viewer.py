"""
Attribute Viewer (UI-only, MVVM, CN-driven).
"""

import FreeCAD
from PySide.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from PySide.QtCore import Qt

from opetreewb.ui.viewmodels.attribute_viewmodel import AttributeViewerViewModel
from opetreewb.domain import CN


class AttributeViewer(QWidget):
    """
    Dockable Attribute Viewer.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vm = AttributeViewerViewModel()

        self.vm.error.connect(self._on_error)
        self.vm.data_changed.connect(self._refresh)
        self.vm.attribute_value_changed.connect(
            self._on_attribute_value_changed
        )

        # CN is the single source of truth
        CN.changed.connect(self._on_cn_changed)

        self._building = False
        self._build_ui()

        self.table.itemChanged.connect(self._on_table_item_changed)

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
    # CN handling
    # -------------------------------------------------
    def _on_cn_changed(self, node):
        # Delegate node → attributes transformation to VM
        self.vm.set_current_node(node)

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

    # -------------------------------------------------
    # Editing
    # -------------------------------------------------
    def _on_table_item_changed(self, item):
        if self._building:
            return

        if item.column() != 1:
            return

        row_index = item.row()
        new_value = item.text()

        old_value = self.vm.get_rows()[row_index].value
        
        # View → ViewModel → CN → AttributeService
        ok = self.vm.update_value(row_index, new_value)
        if not ok:
            # revert UI
            self._building = True
            item.setText(old_value)
            self._building = False

    def _on_attribute_value_changed(self, data_id: int, new_value: str):
        FreeCAD.Console.PrintMessage(
            f"[AttributeViewer] Attribute changed: data_id={data_id}, value={new_value}\n"
        )

    def _on_error(self, msg: str):
        FreeCAD.Console.PrintError(f"❌ {msg}\n")