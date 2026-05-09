from PySide import QtCore
from opetreewb.ui.model.connection_model import ConnectionFormModel

# ✅ NEW
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from OPE_DB_API.config.loader import set_client_config_file

from pathlib import Path


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
        # -------- UI validation --------
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
        self.model.project_code = project_code.upper()
        self.model.domain = domain.upper()
        self.model.local_db_host = local_db_host
        self.model.local_db_port = local_db_port
        self.model.local_db_name = local_db_name
        self.model.local_db_user = local_db_user
        self.model.local_db_password = local_db_password

        try:
            # ✅ ✅ ✅ STEP 1 — Configure GLOBAL CONTEXT
            OPE_DB_CONTEXT.configure(
                code=self.model.project_code,
                domain=self.model.domain,
                username="FreeCADUser",
                hostname="FREECAD",
            )

            # ✅ ✅ ✅ STEP 2 — Configure API Base URL
            OPE_DB_CONTEXT._api_url = self.model.api_url.rstrip("/")

            # ✅ ✅ ✅ STEP 3 — Configure local DB (dynamic config)
            client_config = {
                "database_map": {
                    self.model.project_code: "local_dynamic_db"
                },
                "local_dynamic_db": {
                    "user": self.model.local_db_user,
                    "password": self.model.local_db_password,
                    "host": self.model.local_db_host,
                    "port": int(self.model.local_db_port),
                    "database": self.model.project_code.lower(),
                },
            }

            # ✅ write temp config file
            config_path = Path.home() / ".opetreewb_client_config.toml"

            import toml
            with open(config_path, "w") as f:
                toml.dump(client_config, f)

            # ✅ register config
            set_client_config_file(config_path)

        except Exception as e:
            self.error.emit(f"Failed to configure system: {e}")
            return

        # -------- Emit success --------
        self.success.emit({
            "api_url": api_url,
            "project_code": self.model.project_code,
            "domain": self.model.domain,
            "local_db_host": local_db_host,
            "local_db_port": local_db_port,
            "local_db_name": local_db_name,
            "local_db_user": local_db_user,
            "local_db_password": "***",
        })