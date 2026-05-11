from datetime import datetime

import FreeCAD

from opetreewb.domain.services.service_locator import (
    get_sync_service,
    get_session_service
)
from opetreewb.domain import CN

class SyncSnapshotCommand:
    """
    Fetch authoritative snapshot from server
    and store it into local LIVE tables.
    """

    def GetResources(self):
        return {
            "MenuText": "Sync Snapshot",
            "ToolTip": "Sync full subtree snapshot from server",
        }

    def IsActive(self):
        return get_session_service().is_session_active()

    def Activated(self):
        try:
            rows = get_sync_service().sync_snapshot(CN.id)
            FreeCAD.Console.PrintMessage(
                f"✅ Snapshot synced ({len(rows)} rows)\n"
            )

        except Exception as exc:
            FreeCAD.Console.PrintError(
                f"❌ Snapshot sync failed: {exc}\n"
            )


class SyncHistoryCommand:
    """
    Fetch committed history from server using session-based sync cursor.

    Current behavior:
    - Initializes last_synced_at on first sync
    - Fetches history AFTER cursor timestamp
    - Does NOT apply history to LIVE yet (safe testing stage)
    """

    def GetResources(self):
        return {
            "MenuText": "Sync History",
            "ToolTip": "Sync committed history from server",
        }

    def IsActive(self):
        return get_session_service().is_session_active()

    def Activated(self):
        try:
            after_ts = datetime.now()
            FreeCAD.Console.PrintMessage(
                f"ℹ️ History sync cursor = {after_ts.isoformat()}\n"
            )

            rows = 0
            get_sync_service().sync_history()
            FreeCAD.Console.PrintMessage(
                f"✅ History fetched ({len(rows)} rows)\n"
            )

            FreeCAD.Console.PrintMessage(
                f"✅ new_ts is updated in Session Table\n"
            )

        except Exception as exc:
            import traceback
            traceback.print_exc()
            FreeCAD.Console.PrintError(
                f"❌ History sync failed: {exc}\n"
            )
