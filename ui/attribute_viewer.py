# ui/attribute_viewer.py
"""
Attribute Viewer.

Displays attributes of the global Current Node (CN).
Listens to CN changes and updates automatically.
"""

from PySide.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from PySide.QtCore import Qt

from OPETreeWB.core.cn_manager import CN


class AttributeViewer(QWidget):
    """
    Attribute Viewer panel.

    Shows all available attributes for the current CN (ElementRef).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._row_to_attr = {}
        self._build_ui()

        # Listen to CN changes
        CN.changed.connect(self._on_cn_changed)

    # ---------------------------------------------------------
    # UI setup
    # ---------------------------------------------------------
    def _build_ui(self):
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Attribute", "Value"])

        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setEditTriggers(
            QTableWidget.DoubleClicked |
            QTableWidget.EditKeyPressed
        )
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def clear(self):
        """
        Clear the attribute table.
        """
        self.table.setRowCount(0)

    # ---------------------------------------------------------
    # CN handling
    # ---------------------------------------------------------
    def _on_cn_changed(self, element_ref):
        """
        Slot called when CN changes.
        """
        self.clear()

        if element_ref is None:
            return

        self.table.blockSignals(True)
        self._row_to_attr.clear()

        for row, key in enumerate(element_ref.keys()):
            try:
                value = element_ref[key]
            except Exception as exc:
                value = f"<ERROR: {exc}>"

            self.table.insertRow(row)

            # Attribute name (read-only)
            key_item = QTableWidgetItem(str(key))
            key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, key_item)

            # Attribute value (editable)
            val_item = QTableWidgetItem(str(value))
            self.table.setItem(row, 1, val_item)

            self._row_to_attr[row] = key

        self.table.blockSignals(False)

    def _coerce_value(self, element_ref, attr_key, text_value):
        """
        Convert text input into correct Python type
        based on existing attribute value.
        """
        try:
            old_value = element_ref[attr_key]
        except Exception:
            return text_value
    
        # Boolean
        if isinstance(old_value, bool):
            return text_value.lower() in ("1", "true", "yes", "on")
    
        # Number
        if isinstance(old_value, int):
            return int(text_value)
    
        if isinstance(old_value, float):
            return float(text_value)
    
        # Array / others → string fallback
        return text_value