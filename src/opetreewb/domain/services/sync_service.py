from datetime import datetime
from opetreewb.messaging.reporter import Reporter
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient

class SyncService:
    """
    Handles snapshot and history sync.
    """
    def __init__(self, fcadclient:OpeDBClient=None):
        self.opeclient = fcadclient

    def sync_snapshot(self):
        Reporter.info("[SyncService] snapshot sync requested")
        self.opeclient.sync_get_snapshot_api()
        Reporter.success("[SyncService] snapshot sync completed")
        self.opeclient.sync_set_snapshot_local()

    def sync_history(self):
        ts = datetime.now().isoformat()
        Reporter.info(f"[SyncService] history sync requested (after={ts})")
        self.opeclient.sync_get_history_api()
        Reporter.success("[SyncService] history sync completed")
        self.opeclient.sync_set_history_local()