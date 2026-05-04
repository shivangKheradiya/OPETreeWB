"""
AttributeViewerViewModel (UI only)

- Supplies attribute data
- Validates edits
- Emits messages for UI
"""

from PySide import QtCore
from opetreewb.ui.attribute_model import (
    AttributeTableModel,
    AttributeRow,
)


class AttributeViewerViewModel(QtCore.QObject):
    data_changed = QtCore.Signal()
    error = QtCore.Signal(str)
    message = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.model = AttributeTableModel()

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

        row.value = new_value
        self.message.emit(
            f"Attribute '{row.attribute}' updated to '{new_value}'"
        )
        self.data_changed.emit()
