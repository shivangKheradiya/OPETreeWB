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
    QMessageBox,
)
from PySide.QtCore import Qt

from OPETreeWB.core.cn_manager import CN
from OPETreeWB.core.app_context import APP_CONTEXT
from OPETreeWB.core.data_access import OPEDataAccess
from OPETreeWB.facades.attribute_facade import AttributeFacade

USE_ATTRIBUTE_FACADE = True
DEBUG_ATTRIBUTE_FACADE = True
USE_WORKING_VIEW = True  # Toggle this to False to rollback

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
        node_id = int(element_ref.id)

        data_access = OPEDataAccess(provider)
        data_access = OPEDataAccess(provider)

        if USE_ATTRIBUTE_FACADE:
            self.facade = AttributeFacade(
                provider,
                data_access,
                debug=DEBUG_ATTRIBUTE_FACADE,
            )
            rows = self.facade.get_attributes(node_id)
        else:
            # OLD PATH (baseline comparison)
            data_access.ensure_node_loaded(node_id)
            rows = data_access.get_node_attributes_local(node_id)

        if not rows:
            return

        self._building = True
        self.table.blockSignals(True)
        self._row_to_attr.clear()

        if USE_ATTRIBUTE_FACADE:
            editable = self.facade.is_editable()
        else:
            editable = provider._session_id is not None

        self.table.setEditTriggers(
            QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed
            if editable
            else QTableWidget.NoEditTriggers
        )

        node_id = element_ref.id
        
        self.table.setRowCount(0)
        for row_idx, row in enumerate(rows):
            attr_id = row["attribute_id"]
            value = row["value"]
            data_id = row["data_id"]
        
            attr_name = provider.registry.get_name(attr_id)
        
            self.table.insertRow(row_idx)
        
            key_item = QTableWidgetItem(attr_name)
            key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 0, key_item)
        
            val_item = QTableWidgetItem(str(value))
            if not editable or attr_name in ("Type", "Owner"):
                val_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row_idx, 1, val_item)
        
            data_item = QTableWidgetItem(str(data_id))
            data_item.setFlags(data_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 2, data_item)
        
            self._row_to_attr[row_idx] = {
                "attribute_id": attr_id,
                "data_id": data_id,
                "attribute_name": attr_name,
            }

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

        row_info = self._row_to_attr[row]
        attr_name = row_info["attribute_name"]
        new_text = item.text()

        try:
            value = self._coerce_value(
                element_ref,
                attr_name,
                new_text,
            )

            # ✅ THIS is the real binding
            if USE_ATTRIBUTE_FACADE:
                self.facade.update_attribute(element_ref, attr_name, value)
            else:
                element_ref[attr_name] = value

            # ✅ Notify others (tree) about attribute change
            CN.attributeChanged.emit(element_ref, attr_name)
            self._on_cn_changed(element_ref)

        except Exception as exc:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Update failed",
                str(exc),
            )