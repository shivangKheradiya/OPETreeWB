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
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    # ---------------------------------------------------------
    # CN handling
    # ---------------------------------------------------------
    def _on_cn_changed(self, element_ref):
        """
        Slot called when CN changes.
        """
        if element_ref is None:
            self.clear()
            return

        for key in element_ref.keys():
            value = element_ref[key]

