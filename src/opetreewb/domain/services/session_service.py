from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.session_state import SessionState

class SessionService:
    """
    Manages OPE session lifecycle.
    """

    # Temporary in-memory state (backend will replace this later)
    def __init__(self, opeclient=None):

        # ✅ Facade (API + LOCAL)
        self.opeclient = opeclient

        # ✅ UI state tracking
        self._state = SessionState.NO_SESSION

    def start(self):
        Reporter.success("[SessionService] session start requested")
        # TODO: legacy provider.start_session()
        self._state = SessionState.ACTIVE
        Reporter.success(f"Session state → {self._state.name}")

    def commit(self):
        Reporter.success("[SessionService] session commit requested")
        # TODO: legacy provider.commit_session()
        self._state = SessionState.COMMITTED
        Reporter.success(f"Session state → {self._state.name}")

    def abort(self):
        Reporter.warning("[SessionService] session abort requested")
        # TODO: legacy provider.abort_session()
        self._state = SessionState.ABORTED
        Reporter.success(f"Session state → {self._state.name}")

    def is_session_active(self) -> bool:
        return self._state == SessionState.ACTIVE
