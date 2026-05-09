"""
Connection and Project Selection Dialog (UI only).

- Messages are printed to FreeCAD Report View
"""

from PySide import QtWidgets
import FreeCAD

from opetreewb.ui.viewmodels.connection_viewmodel import ConnectionViewModel
from opetreewb.domain.services.service_container import ServiceContainer
from opetreewb.app.app_context import AppContext


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OPE Connection Setup")
        self.setModal(True)
        self.resize(420, 260)

        self.vm = ConnectionViewModel()
        self.vm.error.connect(self._report_error)
        self.vm.success.connect(self._on_success)

        self._build_ui()
        self._load_from_vm()

    # -------------------------------------------------
    # UI construction
    # -------------------------------------------------
    def _build_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self.api_url_edit = QtWidgets.QLineEdit()
        self.project_code_edit = QtWidgets.QLineEdit()

        self.domain_combo = QtWidgets.QComboBox()
        self.domain_combo.addItems([
            "SKET",
            "DESI",
            "DICT",
        ])

        layout.addRow("API Base URL:", self.api_url_edit)
        layout.addRow("Project Code:", self.project_code_edit)
        layout.addRow("Domain:", self.domain_combo)

        layout.addRow(QtWidgets.QLabel("<b>Local Cache Database</b>"))

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

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    # -------------------------------------------------
    # Load dummy data
    # -------------------------------------------------
    def _load_from_vm(self):
        data = self.vm.get_initial_values()

        self.api_url_edit.setText(data["api_url"])
        self.project_code_edit.setText(data["project_code"])
        self.local_db_host_edit.setText(data["local_db_host"])
        self.local_db_port_edit.setText(str(data["local_db_port"]))
        self.local_db_name_edit.setText(data["local_db_name"])
        self.local_db_user_edit.setText(data["local_db_user"])
        self.local_db_password_edit.setText(data["local_db_password"])

        idx = self.domain_combo.findText(data["domain"])
        if idx >= 0:
            self.domain_combo.setCurrentIndex(idx)

    # -------------------------------------------------
    # Events
    # -------------------------------------------------
    def _on_accept(self):
        self.vm.apply(
            api_url=self.api_url_edit.text().strip(),
            project_code=self.project_code_edit.text().strip(),
            domain=self.domain_combo.currentText(),
            local_db_host=self.local_db_host_edit.text().strip(),
            local_db_port=self.local_db_port_edit.text().strip(),
            local_db_name=self.local_db_name_edit.text().strip(),
            local_db_user=self.local_db_user_edit.text().strip(),
            local_db_password=self.local_db_password_edit.text(),
        )

    # -------------------------------------------------
    # Report View output
    # -------------------------------------------------
    def _report_error(self, msg: str):
        FreeCAD.Console.PrintError(
            f"[ConnectionDialog] ERROR: {msg}\n"
        )

    def _on_success(self, data: dict):
        FreeCAD.Console.PrintMessage(
            "[ConnectionDialog] Connection parameters accepted:\n"
        )
        
        AppContext.container = ServiceContainer()

        # =================================================
        # ✅ START SESSION
        # =================================================
        FreeCAD.Console.PrintMessage(
            "[ConnectionDialog] Starting session...\n"
        )
        
        success = AppContext.container.session_service.start()

        if not success:
            FreeCAD.Console.PrintError(
                "[ConnectionDialog] Session start FAILED ❌\n"
            )
            return

        FreeCAD.Console.PrintMessage(
            "[ConnectionDialog] Session started ✅\n"
        )

        self.accept()