import FreeCAD
from PySide.QtCore import Qt
from PySide.QtWidgets import (QDialog, QHBoxLayout, QListWidget,
                              QListWidgetItem, QPushButton, QVBoxLayout)

from opetreewb.tests.run_tests import list_tests, run_all, run_selected


class TestRunnerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OPETreeWB Test Runner")
        self.resize(400, 300)

        self._build_ui()
        self._populate_tests()

    # -------------------------------
    # UI
    # -------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.test_list = QListWidget()
        self.test_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.test_list)

        button_row = QHBoxLayout()

        self.run_selected_btn = QPushButton("Run Selected")
        self.run_all_btn = QPushButton("Run All")
        self.close_btn = QPushButton("Close")

        button_row.addWidget(self.run_selected_btn)
        button_row.addWidget(self.run_all_btn)
        button_row.addWidget(self.close_btn)

        layout.addLayout(button_row)

        self.run_selected_btn.clicked.connect(self._on_run_selected)
        self.run_all_btn.clicked.connect(self._on_run_all)
        self.close_btn.clicked.connect(self.close)

    # -------------------------------
    # Data
    # -------------------------------
    def _populate_tests(self):
        self.test_list.clear()
        for test_id in list_tests():
            item = QListWidgetItem(test_id)
            item.setCheckState(Qt.Unchecked)
            self.test_list.addItem(item)

    # -------------------------------
    # Actions
    # -------------------------------
    def _on_run_all(self):
        FreeCAD.Console.PrintMessage("\n[OPETreeWB] Running ALL tests\n")
        run_all()

    def _on_run_selected(self):
        selected = []
        for i in range(self.test_list.count()):
            item = self.test_list.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())

        if not selected:
            FreeCAD.Console.PrintWarning("[OPETreeWB] No tests selected\n")
            return

        FreeCAD.Console.PrintMessage(
            f"\n[OPETreeWB] Running selected tests: {selected}\n"
        )

        run_selected(selected)
