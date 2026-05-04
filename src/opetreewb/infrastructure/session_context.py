"""
SessionContext

Single source of truth for the currently active session
and provider inside OPETreeWB.

Design goals:
- Explicit state
- No FreeCAD dependencies
- No UI logic
- Easy to test
"""

class SessionContext:
    def __init__(self):
        self._provider = None

    # -----------------------------
    # Provider handling
    # -----------------------------

    def set_provider(self, provider):
        """
        Set the active provider for the current session.
        """
        self._provider = provider

    def clear_provider(self):
        """
        Clear the active provider and session.
        """
        self._provider = None

    def get_provider(self):
        """
        Return the active provider, or None.
        """
        return self._provider

    # -----------------------------
    # Session state helpers
    # -----------------------------

    def has_provider(self) -> bool:
        return self._provider is not None
