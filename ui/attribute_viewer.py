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
        self.table.itemChanged.connect(self._on_item_changed)

    # ---------------------------------------------------------
    # UI setup
    # ---------------------------------------------------------
    def _build_ui(self):
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Attribute", "Value", "Data ID"])

        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setEditTriggers(
            QTableWidget.DoubleClicked |
            QTableWidget.EditKeyPressed
        )
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # self.table.setColumnHidden(2, True)
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
       self.clear()

       if element_ref is None:
           return

       self.table.blockSignals(True)
       self._row_to_attr.clear()

       provider = element_ref._provider
       node_id = element_ref.id

       # ✅ Access provider cache: { attr_id: (data_id, value) }
       cache = provider._cache.get(node_id, {})

       for row, attr_id in enumerate(cache.keys()):
           attr_name = provider.registry.get_name(attr_id)
           data_id, value = cache[attr_id]

           self.table.insertRow(row)

           # Attribute name (read-only)
           key_item = QTableWidgetItem(attr_name)
           key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
           self.table.setItem(row, 0, key_item)

           # Attribute value (editable)
           val_item = QTableWidgetItem(str(value))
           self.table.setItem(row, 1, val_item)

           # ✅ Data ID (hidden column)
           data_item = QTableWidgetItem(str(data_id))
           data_item.setFlags(data_item.flags() & ~Qt.ItemIsEditable)
           self.table.setItem(row, 2, data_item)

           # ✅ Map row → attribute name
           self._row_to_attr[row] = attr_name

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
    
    
    def _on_item_changed(self, item):
        # Only react to Value column
        if item.column() != 1:
            return

        row = item.row()
        if row not in self._row_to_attr:
            return

        element_ref = CN()
        if element_ref is None:
            return

        attr_name = self._row_to_attr[row]
        new_text = item.text()

        try:
            value = self._coerce_value(
                element_ref,
                attr_name,
                new_text,
            )

            # ✅ THIS is the real binding
            element_ref[attr_name] = value

        except Exception as exc:
            QtWidgets.QMessageBox.critical(
                self,
                "Update failed",
                str(exc),
            )