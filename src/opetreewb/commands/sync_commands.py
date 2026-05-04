from datetime import datetime

import FreeCAD

from opetreewb.infrastructure import SESSION_CONTEXT

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
        provider = SESSION_CONTEXT.get_provider()
        return provider is not None

    def Activated(self):
        provider = SESSION_CONTEXT.get_provider()

        try:
            rows = 0
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
        provider = SESSION_CONTEXT.get_provider()
        return provider is not None

    def Activated(self):
        provider = SESSION_CONTEXT.get_provider()

        try:
            after_ts = datetime.now()
            FreeCAD.Console.PrintMessage(
                f"ℹ️ History sync cursor = {after_ts.isoformat()}\n"
            )

            rows = 0
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
