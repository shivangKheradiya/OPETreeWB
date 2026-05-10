from opetreewb.domain.session_state import SessionState

class SessionRuleResult:
    def __init__(self, allowed: bool, reason: str = ""):
        self.allowed = allowed
        self.reason = reason


class SessionRules:

    @staticmethod
    def can_start(current_state):
        if current_state == SessionState.ACTIVE:
            return SessionRuleResult(False, "Session already active")
        return SessionRuleResult(True)

    @staticmethod
    def can_commit(current_state):
        if current_state != SessionState.ACTIVE and current_state != SessionState.ABORTED:
            return SessionRuleResult(False, "No active session to commit")
        return SessionRuleResult(True)

    @staticmethod
    def can_abort(current_state):
        if current_state != SessionState.ACTIVE and current_state != SessionState.ABORTED:
            return SessionRuleResult(False, "No active session to abort")
        return SessionRuleResult(True)
