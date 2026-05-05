"""
ConnectionViewModel (UI only)

- Owns the ConnectionFormModel
- Performs validation
- Emits UI signals
"""

from PySide import QtCore
from opetreewb.ui.model.connection_model import ConnectionFormModel


class ConnectionViewModel(QtCore.QObject):
    error = QtCore.Signal(str)
    success = QtCore.Signal(dict)

    def __init__(self):
        super().__init__()
        self.model = ConnectionFormModel()

    # -----------------------------------------
    # Expose model values to View
    # -----------------------------------------
    def get_initial_values(self) -> dict:
        return self.model.__dict__

    # -----------------------------------------
    # Validate + update model
    # -----------------------------------------
    def apply(
        self,
        api_url: str,
        project_code: str,
        domain: str,
        local_db_host: str,
        local_db_port: str,
        local_db_name: str,
        local_db_user: str,
        local_db_password: str,
    ):
        # -------- UI validation only --------
        if not api_url:
            self.error.emit("API Base URL is required")
            return

        if not project_code:
            self.error.emit("Project Code is required")
            return

        if not domain:
            self.error.emit("Domain must be selected")
            return

        if local_db_port and not local_db_port.isdigit():
            self.error.emit("Local DB Port must be numeric")
            return

        # -------- Update model --------
        self.model.api_url = api_url
        self.model.project_code = project_code
        self.model.domain = domain
        self.model.local_db_host = local_db_host
        self.model.local_db_port = local_db_port
        self.model.local_db_name = local_db_name
        self.model.local_db_user = local_db_user
        self.model.local_db_password = local_db_password

        # Emit sanitized output (UI feedback only)
        self.success.emit({
            "api_url": api_url,
            "project_code": project_code,
            "domain": domain,
            "local_db_host": local_db_host,
            "local_db_port": local_db_port,
            "local_db_name": local_db_name,
            "local_db_user": local_db_user,
            "local_db_password": "***",
        })