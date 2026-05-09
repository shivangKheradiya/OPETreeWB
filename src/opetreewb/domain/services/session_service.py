from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.session_state import SessionState
from opetreewb.domain.transection.transaction_manager import TransactionManager
from opetreewb.domain.rules.session_rules import SessionRules
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient
from opetreewb.domain.transection.transaction_result import TransactionResult

class SessionService:
    """
    Manages OPE session lifecycle (explicit API + LOCAL control).
    """

    def __init__(self, opeclient:OpeDBClient=None):

        self.opeclient = opeclient
        self.tx = TransactionManager()
        self._state = SessionState.NO_SESSION

    # -------------------------------------------------
    # START
    # -------------------------------------------------
    def start(self):

        result = SessionRules.can_start(self._state)

        if not result.allowed:
            Reporter.error(
                f"[SessionService] Start denied: {result.reason}"
            )
            return False

        # -------------------------
        def server_op():

            Reporter.info("[SERVER] Calling API start_session")

            try:
                if not self.opeclient:
                    raise RuntimeError("No OpeDBClient configured")

                session_id = self.opeclient.start_session_api()
                return TransactionResult(success=True, message=session_id)

            except Exception as e:
                Reporter.error(f"[SERVER] start_session_api failed → {e}")
                raise

        # -------------------------
        def local_op():

            Reporter.info("[LOCAL] Calling local start_session")

            try:
                self.opeclient.start_session_local()

                self._state = SessionState.ACTIVE

                Reporter.info(
                    f"[LOCAL] Session active)"
                )
                return TransactionResult(success=True, message="Added into Local Db")

            except Exception as e:
                Reporter.error(f"[LOCAL] start_session_local failed → {e}")
                raise

        # -------------------------
        tx_result = self.tx.run(server_op, local_op, "Start Session")

        if not tx_result.success:
            return False

        Reporter.success("[SessionService] Session STARTED")

        return True

    # -------------------------------------------------
    # COMMIT
    # -------------------------------------------------
    def commit(self):

        result = SessionRules.can_commit(self._state)

        if not result.allowed:
            Reporter.error(
                f"[SessionService] Commit denied: {result.reason}"
            )
            return False

        # -------------------------
        def server_op():

            Reporter.info("[SERVER] Calling API commit_session")

            try:
                result = self.opeclient.commit_session_api()
                return TransactionResult(success=True, message=result)
            except Exception as e:
                Reporter.error(f"[SERVER] commit_session_api failed → {e}")
                raise

        # -------------------------
        def local_op():

            Reporter.info("[LOCAL] Calling local commit_session")

            try:
                result = self.opeclient.commit_session_local()

                self._state = SessionState.COMMITTED

                Reporter.info("[LOCAL] Session committed")
                return TransactionResult(success=True, message=result)
            
            except Exception as e:
                Reporter.error(f"[LOCAL] commit_session_local failed → {e}")
                raise

        # -------------------------
        tx_result = self.tx.run(server_op, local_op, "Commit Session")

        if not tx_result.success:
            return False

        Reporter.success("[SessionService] Session COMMITTED")

        return True

    # -------------------------------------------------
    # ABORT
    # -------------------------------------------------
    def abort(self):

        result = SessionRules.can_abort(self._state)

        if not result.allowed:
            Reporter.error(
                f"[SessionService] Abort denied: {result.reason}"
            )
            return False

        # -------------------------
        def server_op():

            Reporter.warning("[SERVER] Calling API abort_session")

            try:
                result = self.opeclient.abort_session_api()
                return TransactionResult(success=True, message=result)
            except Exception as e:
                Reporter.error(f"[SERVER] abort_session_api failed → {e}")
                raise

        # -------------------------
        def local_op():

            Reporter.info("[LOCAL] Calling local abort_session")

            try:
                result = self.opeclient.abort_session_local()

                self._state = SessionState.ABORTED

                Reporter.info("[LOCAL] Session aborted")
                return TransactionResult(success=True, message=result)
            except Exception as e:
                Reporter.error(f"[LOCAL] abort_session_local failed → {e}")
                raise

        # -------------------------
        tx_result = self.tx.run(server_op, local_op, "Abort Session")

        if not tx_result.success:
            return False

        Reporter.success("[SessionService] Session ABORTED")

        return True

    # -------------------------------------------------
    def is_session_active(self) -> bool:
        return self._state == SessionState.ACTIVE or self._state == SessionState.ABORTED