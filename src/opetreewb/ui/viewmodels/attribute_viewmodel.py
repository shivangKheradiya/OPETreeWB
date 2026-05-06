"""
AttributeViewerViewModel

- Supplies attribute data
- Validates edits
- Delegates mutations through CN
"""

from PySide import QtCore
from opetreewb.ui.model.attribute_model import (
    AttributeTableModel,
    AttributeRow,
)
from opetreewb.domain import CN


class AttributeViewerViewModel(QtCore.QObject):
    data_changed = QtCore.Signal()
    error = QtCore.Signal(str)
    message = QtCore.Signal(str)
    attribute_value_changed = QtCore.Signal(int, str)

    def __init__(self):
        super().__init__()
        self.model = AttributeTableModel()
        self._current_node = None

    # -----------------------------------------
    # CN-driven input
    # -----------------------------------------
    def set_current_node(self, node):
        """Called when CN changes."""
        self._current_node = node
        self.model.clear()

        if node is None:
            self.data_changed.emit()
            return

        for attr_name, attr_value in node.attributes.items():
            self.model.rows.append(
                AttributeRow(
                    attribute=attr_name,
                    value=str(attr_value.value),
                    data_id=attr_value.data_id,
                )
            )

        self.data_changed.emit()

    # -----------------------------------------
    # Data access
    # -----------------------------------------
    def get_rows(self):
        return self.model.rows

    # -----------------------------------------
    # Handle edits (delegate to CN)
    # -----------------------------------------
    def update_value(self, row_index: int, new_value: str):
        if row_index >= len(self.model.rows):
            self.error.emit("Invalid row index")
            return

        row = self.model.rows[row_index]

        # UI‑level validation
        if row.attribute in ("Type", "Owner"):
            self.error.emit(
                f"'{row.attribute}' is read-only"
            )
            return False

        old_value = row.value
        if new_value == old_value:
            return

        # ✅ Delegate mutation to CN
        data_id = row.data_id if hasattr(row, "data_id") else None

        ok = CN.set_attr(row.attribute, new_value, data_id)
        if not ok:
            return False

        # ✅ Keep UI model in sync
        row.value = new_value

        self.attribute_value_changed.emit(
            row.data_id,
            new_value,
        )

        self.message.emit(
            f"Attribute '{row.attribute}' updated to '{new_value}'"
        )
        self.data_changed.emit()