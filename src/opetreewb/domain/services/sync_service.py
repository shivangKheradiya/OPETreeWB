from datetime import datetime
from opetreewb.messaging.reporter import Reporter


class SyncService:
    """
    Handles snapshot and history sync.
    """

    def sync_snapshot(self):
        Reporter.info("[SyncService] snapshot sync requested")
        # TODO: legacy snapshot sync
        Reporter.success("[SyncService] snapshot sync completed")

    def sync_history(self):
        ts = datetime.now().isoformat()
        Reporter.info(f"[SyncService] history sync requested (after={ts})")
        # TODO: legacy history sync
        Reporter.success("[SyncService] history sync completed")