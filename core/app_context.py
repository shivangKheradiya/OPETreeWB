# core/app_context.py
"""
Global application context for OPETreeWB.

Stores connection and project-level information required
to create PyDBML providers.
"""


class AppContext:
    def __init__(self):
        self.api_url = None
        self.project_code = None
        self.domain = None
        self.username = None
        self.hostname = None

    # ----------------------------
    # Convenience helpers
    # ----------------------------
    def is_configured(self) -> bool:
        return bool(self.api_url and self.project_code and self.domain)

    def clear(self):
        self.api_url = None
        self.project_code = None
        self.domain = None
        self.username = None
        self.hostname = None


# -------------------------------------------------
# Singleton context (global state)
# -------------------------------------------------
APP_CONTEXT = AppContext()