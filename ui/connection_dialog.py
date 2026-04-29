# ui/connection_dialog.py
"""
Connection and Project Selection Dialog.
"""

from PySide import QtWidgets
from OPETreeWB.core.app_context import APP_CONTEXT
from OPETreeWB.core.context_store import save_context, load_context

class ConnectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OPE Connection Setup")
        self.setModal(True)
        self.resize(420, 260)

        load_context()
        
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
            "DICT",
            "HIER",
        ])

        layout.addRow("API Base URL:", self.api_url_edit)
        layout.addRow("Project Code:", self.project_code_edit)
        layout.addRow("Domain:", self.domain_combo)

        layout.addRow(QtWidgets.QLabel("<b>Local Cache Database</b>"))
        # -----------------------------
        # Local DB (Client Cache)
        # -----------------------------
        self.local_db_host_edit = QtWidgets.QLineEdit()
        self.local_db_port_edit = QtWidgets.QLineEdit()
        self.local_db_name_edit = QtWidgets.QLineEdit()
        self.local_db_user_edit = QtWidgets.QLineEdit()
        self.local_db_password_edit = QtWidgets.QLineEdit()
        self.local_db_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        layout.addRow("Local DB Host:", self.local_db_host_edit)
        layout.addRow("Local DB Port:", self.local_db_port_edit)
        layout.addRow("Local DB Name:", self.local_db_name_edit)
        layout.addRow("Local DB User:", self.local_db_user_edit)
        layout.addRow("Local DB Password:", self.local_db_password_edit)

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
        # -----------------------------
        # API URL
        # -----------------------------
        if APP_CONTEXT.api_url:
            self.api_url_edit.setText(APP_CONTEXT.api_url)
        else:
            self.api_url_edit.setText("http://127.0.0.1:8000/")
    
        # -----------------------------
        # Project code
        # -----------------------------
        if APP_CONTEXT.project_code:
            self.project_code_edit.setText(APP_CONTEXT.project_code)
        else:
            self.project_code_edit.setText("XYZ")
    
        # -----------------------------
        # Domain
        # -----------------------------
        if APP_CONTEXT.domain:
            idx = self.domain_combo.findText(APP_CONTEXT.domain)
            if idx >= 0:
                self.domain_combo.setCurrentIndex(idx)
    
        # -----------------------------
        # Root node ID (optional / legacy)
        # -----------------------------
        if APP_CONTEXT.root_node_id is not None:
            self.root_node_id_edit.setText(str(APP_CONTEXT.root_node_id))

        
        # -----------------------------
        # Local DB defaults
        # -----------------------------
        self.local_db_host_edit.setText(
            APP_CONTEXT.local_db_host or "localhost"
        )
        self.local_db_port_edit.setText(
            str(APP_CONTEXT.local_db_port or 5433)
        )
        self.local_db_name_edit.setText(
            APP_CONTEXT.local_db_name or "xyz"
        )
        self.local_db_user_edit.setText(
            APP_CONTEXT.local_db_user or "postgres"
        )
        self.local_db_password_edit.setText(
            APP_CONTEXT.local_db_password or "postgres"
        )

    def _on_accept(self):
        # Read values
        api_url = self.api_url_edit.text().strip()
        project_code = self.project_code_edit.text().strip()
        domain = self.domain_combo.currentText()

        # Store in global context
        APP_CONTEXT.api_url = api_url
        APP_CONTEXT.project_code = project_code
        APP_CONTEXT.domain = domain

        # -----------------------------
        # Local DB settings
        # -----------------------------
        APP_CONTEXT.local_db_host = self.local_db_host_edit.text().strip()
        APP_CONTEXT.local_db_port = int(self.local_db_port_edit.text())
        APP_CONTEXT.local_db_name = self.local_db_name_edit.text().strip()
        APP_CONTEXT.local_db_user = self.local_db_user_edit.text().strip()
        APP_CONTEXT.local_db_password = self.local_db_password_edit.text()

        save_context()   # ✅ store in temp
        
        self.accept()