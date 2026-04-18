# ui/connection_dialog.py
"""
Connection and Project Selection Dialog.
"""

from PySide import QtWidgets
from OPETreeWB.core.app_context import APP_CONTEXT


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OPE Connection Setup")
        self.setModal(True)
        self.resize(420, 260)

        self._build_ui()
        self._load_existing_values()

    # -------------------------------------------------
    # UI construction
    # -------------------------------------------------
    def _build_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self.api_url_edit = QtWidgets.QLineEdit()
        self.project_code_edit = QtWidgets.QLineEdit()

        self.domain_combo = QtWidgets.QComboBox()
        self.domain_combo.addItems([
            "DESI",
            "CATA",
            "ENGG",
        ])

        self.root_node_id_edit = QtWidgets.QLineEdit()
        self.root_node_id_edit.setPlaceholderText("e.g. 1001")

        layout.addRow("API Base URL:", self.api_url_edit)
        layout.addRow("Project Code:", self.project_code_edit)
        layout.addRow("Domain:", self.domain_combo)
        layout.addRow("Root Node ID:", self.root_node_id_edit)

        # Buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    # -------------------------------------------------
    # Data handling
    # -------------------------------------------------
    def _load_existing_values(self):
        if APP_CONTEXT.api_url:
            self.api_url_edit.setText(APP_CONTEXT.api_url)

        if APP_CONTEXT.project_code:
            self.project_code_edit.setText(APP_CONTEXT.project_code)

        if APP_CONTEXT.domain:
            idx = self.domain_combo.findText(APP_CONTEXT.domain)
            if idx >= 0:
                self.domain_combo.setCurrentIndex(idx)

        if APP_CONTEXT.root_node_id is not None:
            self.root_node_id_edit.setText(str(APP_CONTEXT.root_node_id))

    def _on_accept(self):
        # Read values
        api_url = self.api_url_edit.text().strip()
        project_code = self.project_code_edit.text().strip()
        domain = self.domain_combo.currentText()
        root_id_text = self.root_node_id_edit.text().strip()

        # Basic validation for root node id
        if root_id_text:
            try:
                root_node_id = int(root_id_text)
            except ValueError:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Invalid Root Node ID",
                    "Root Node ID must be an integer."
                )
                return
        else:
            root_node_id = None

        # Store in global context
        APP_CONTEXT.api_url = api_url
        APP_CONTEXT.project_code = project_code
        APP_CONTEXT.domain = domain
        APP_CONTEXT.root_node_id = root_node_id

        self.accept()