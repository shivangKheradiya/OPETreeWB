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

from opetreewb.ui.attribute_viewmodel import (
    AttributeViewerViewModel,
)


class AttributeViewer(QWidget):
    """
    UI-only Attribute Viewer.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.vm = AttributeViewerViewModel()
        self.vm.data_changed.connect(self._refresh)
        self.vm.error.connect(self._report_error)
        self.vm.message.connect(self._report_message)

        self._building = False
        self._build_ui()
        self._refresh()

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
        self.table.itemChanged.connect(
            self._on_item_changed
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

        for row_idx, row in enumerate(rows):
            self._set_item(row_idx, 0, row.attribute, False)
            self._set_item(row_idx, 1, row.value, True)
            self._set_item(row_idx, 2, row.data_id, False)

        self.table.blockSignals(False)
        self._building = False

    def _set_item(self, row, col, text, editable):
        item = QTableWidgetItem(text)
        if not editable:
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(row, col, item)

    # -------------------------------------------------
    # Events
    # -------------------------------------------------
    def _on_item_changed(self, item):
        if self._building:
            return

        if item.column() != 1:
            return

        self.vm.update_value(
            item.row(),
            item.text(),
        )

    # -------------------------------------------------
    # Report View messages
    # -------------------------------------------------
    def _report_error(self, msg: str):
        FreeCAD.Console.PrintError(
            f"[AttributeViewer] ERROR: {msg}\n"
        )

    def _report_message(self, msg: str):
        FreeCAD.Console.PrintMessage(
            f"[AttributeViewer] {msg}\n"
        )