from datetime import datetime
from opetreewb.messaging.reporter import Reporter
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient
from opetreewb.SKET.schema.attribute_ids import get_attr_id

class SyncService:
    """
    Handles snapshot and history sync.
    """
    def __init__(self, fcadclient:OpeDBClient=None):
        self.opeclient = fcadclient

    def sync_snapshot(self, root_node_id):
        Reporter.info("[SyncService] snapshot sync requested")
        rows = self.opeclient.sync_get_snapshot_api(root_node_id, get_attr_id("Owner") )
        Reporter.success("[SyncService] snapshot sync completed")
        self.opeclient.sync_set_snapshot_local()
        return len(rows)

    def sync_history(self):
        ts = datetime.now().isoformat()
        Reporter.info(f"[SyncService] history sync requested (after={ts})")
        self.opeclient.sync_get_history_api(ts)
        Reporter.success("[SyncService] history sync completed")
        self.opeclient.sync_set_history_local()