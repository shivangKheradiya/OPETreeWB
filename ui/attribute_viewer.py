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
from OPETreeWB.core.app_context import APP_CONTEXT

class AttributeViewer(QWidget):
    """
    Attribute Viewer panel.

    Shows all available attributes for the current CN (ElementRef).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._row_to_attr = {}
        self._building = False 
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

        provider = element_ref._provider
        node_id = element_ref.id

        # STEP 2: local-cache check hook (still server-backed)
        provider.ensure_node_loaded(node_id)
        
        self._building = True
        self.table.blockSignals(True)
        self._row_to_attr.clear()

        # ✅ disable editing if no active session
        editable = provider._session_id is not None
        self.table.setEditTriggers(
            QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed
            if editable
            else QTableWidget.NoEditTriggers
        )

        node_id = element_ref.id

        # ✅ Access provider cache: { attr_id: (data_id, value) }
        # cache = provider._cache.get(node_id, {})
        cache = provider._cache.get(node_id)
        if not cache:
            # session ended or data not loaded
            self.table.blockSignals(False)
            return
        
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
            # ✅ Per-attribute editability (future-ready)
            if not editable or attr_name in ("Type", "Owner"):
                val_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 1, val_item)

            # ✅ Data ID (hidden column)
            data_item = QTableWidgetItem(str(data_id))
            data_item.setFlags(data_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, data_item)

            # ✅ Map row → attribute name
            self._row_to_attr[row] = attr_name

        self.table.blockSignals(False)
        self._building = False

    def _coerce_value(self, element_ref, attr_key, text_value):
        provider = element_ref._provider
        attr_id = provider.registry.get_id(attr_key)
        data_type = provider.registry.get_type(attr_id)
    
        if data_type == "String":
            return text_value
    
        if data_type == "Boolean":
            return text_value.lower() in ("1", "true", "yes", "on")
    
        if data_type == "BigInt":
            return int(text_value)
    
        if data_type == "Number":
            return float(text_value)
    
        # fallback
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

            # ✅ Notify others (tree) about attribute change
            CN.attributeChanged.emit(element_ref, attr_name)

        except Exception as exc:
            QtWidgets.QMessageBox.critical(
                self,
                "Update failed",
                str(exc),
            )