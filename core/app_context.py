# core/app_context.py
"""
Global application context for OPETreeWB.

Stores connection and project-level information required
to create PyDBML providers and root tree context.
"""


class AppContext:
    def __init__(self):
        # Connection info
        self.api_url = None
        self.project_code = None
        self.domain = None
        self.username = None
        self.hostname = None

        # Tree context
        self.root_node_id = None

        # -----------------------------
        # Local cache DB (client-side)
        # -----------------------------
        self.local_db_host = None
        self.local_db_port = None
        self.local_db_name = None
        self.local_db_user = None
        self.local_db_password = None

    # -------------------------------------------------
    # Convenience helpers
    # -------------------------------------------------
    def is_configured(self) -> bool:
        """
        Return True if backend configuration is sufficient.
        """
        return bool(
            self.api_url and
            self.project_code and
            self.domain
        )

    def clear(self):
        """
        Reset all context values.
        """
        self.api_url = None
        self.project_code = None
        self.domain = None
        self.username = None
        self.hostname = None
        self.root_node_id = None

        # Local DB
        self.local_db_host = None
        self.local_db_port = None
        self.local_db_name = None
        self.local_db_user = None
        self.local_db_password = None

# -------------------------------------------------
# Singleton context (global state)
# -------------------------------------------------
APP_CONTEXT = AppContext()