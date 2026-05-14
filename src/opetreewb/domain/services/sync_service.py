from datetime import datetime

from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient
from opetreewb.messaging.reporter import Reporter
from opetreewb.SKET.schema.attribute_ids import get_attr_id


class SyncService:
    """
    Handles snapshot and history sync.
    """

    def __init__(self, fcadclient: OpeDBClient = None):
        self.opeclient = fcadclient

    def sync_snapshot(self, root_node_id):
        Reporter.info("[SyncService] snapshot sync requested")
        rows = self.opeclient.sync_get_snapshot_api(root_node_id, get_attr_id("Owner"))
        self.opeclient.sync_set_snapshot_local(rows)
        Reporter.success("[SyncService] snapshot sync completed")
        return rows

    def sync_history(self):
        after_ts = self.opeclient.local_query.get_last_history_sync_ts()
        Reporter.info(f"[SyncService] history sync requested (after={after_ts})")
        rows = self.opeclient.sync_get_history_api(after_ts)
        if not rows:
            Reporter.info("[SyncService] no new history rows")
            return []

        Reporter.success("[SyncService] history sync completed")
        new_ts = self.opeclient.sync_set_history_local(rows)
        self.opeclient.update_last_synced_at_for_active_session(new_ts)
        Reporter.success(f"[SyncService] history sync completed ({len(rows)} rows)")
        return rows
