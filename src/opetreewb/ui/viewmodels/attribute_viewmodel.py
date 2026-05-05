"""
AttributeViewerViewModel

- Supplies attribute data
- Validates edits
- Emits messages for UI
"""

from PySide import QtCore
from opetreewb.ui.model.attribute_model import (
    AttributeTableModel,
    AttributeRow,
)
from opetreewb.domain.attribute_service import AttributeService


class AttributeViewerViewModel(QtCore.QObject):
    data_changed = QtCore.Signal()
    error = QtCore.Signal(str)
    message = QtCore.Signal(str)
    attribute_value_changed = QtCore.Signal(int, str)
    
    def __init__(self):
        super().__init__()
        self.model = AttributeTableModel()
        self.attribute_service = AttributeService()

    # -----------------------------------------
    # Data access
    # -----------------------------------------
    def get_rows(self):
        return self.model.rows

    # -----------------------------------------
    # Handle edits (UI-only)
    # -----------------------------------------
    def update_value(self, row_index: int, new_value: str):
        if row_index >= len(self.model.rows):
            self.error.emit("Invalid row index")
            return

        row = self.model.rows[row_index]

        # UI-only validation
        if row.attribute in ("Type", "Owner"):
            self.error.emit(
                f"'{row.attribute}' is read-only"
            )
            return

        old_value = row.value
        if new_value == old_value:
            return  # no change

        # ✅ Update model
        row.value = new_value

        # ✅ Emit change signal (THIS is what you asked for)
        self.attribute_value_changed.emit(
            row.data_id,
            new_value,
        )

        self.message.emit(
            f"Attribute '{row.attribute}' updated to '{new_value}'"
        )
        self.data_changed.emit()

    def _on_node_selected(self, node):
        import FreeCAD

        FreeCAD.Console.PrintMessage(
            f"[AttributeViewerVM] Node received: {node.label}\n"
        )

        self.model.clear()

        for attr_name, attr_value in node.attributes.items():
            self.model.rows.append(
                AttributeRow(
                    attribute=attr_name,
                    value=str(attr_value.value),   # ✅ FIX: unwrap value
                    data_id=attr_value.data_id,    # ✅ correct data_id
                )
            )

        self.data_changed.emit()
