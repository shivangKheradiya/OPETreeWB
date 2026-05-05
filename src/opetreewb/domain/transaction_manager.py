from opetreewb.messaging.reporter import Reporter
from opetreewb.domain.transaction_result import TransactionResult


class TransactionManager:
    """
    Enforces:
    - server operation first
    - local operation only on success
    """

    def run(self, server_op, local_op, description: str) -> TransactionResult:
        Reporter.info(f"[TX] Server operation started: {description}")

        # ---- SERVER PHASE (dummy for now) ----
        server_result = server_op()

        if not server_result.success:
            Reporter.error(
                f"[TX] Server failed: {server_result.message}"
            )
            return server_result

        Reporter.success("[TX] Server succeeded, applying local transaction")

        # ---- LOCAL PHASE ----
        local_op()

        Reporter.success("[TX] Local transaction applied")
        return TransactionResult(True, "Success")