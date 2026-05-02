import FreeCAD

from OPETreeWB.commands.session_commands import get_active_provider
from OPETreeWB.core.app_context import APP_CONTEXT

from OPETreeWB.core.sync.snapshot_sync import apply_snapshot
from OPETreeWB.core.sync.history_sync import apply_history
from OPETreeWB.core.cn_manager import CN

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
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return

        element_ref = CN()
        if element_ref is None:
            FreeCAD.Console.PrintError(
                "No node selected. Select a node in the tree and retry.\n"
            )
            return

        root_node_id = int(element_ref.id)

        try:
            # ✅ 1. Fetch from server (PyDBML)
            rows = provider.fetch_snapshot(root_node_id)

            # ✅ 2. Persist locally (OPETreeWB)
            apply_snapshot(provider, rows)

            FreeCAD.Console.PrintMessage(
                f"✅ Snapshot synced ({len(rows)} rows)\n"
            )

        except Exception as exc:
            FreeCAD.Console.PrintError(
                f"❌ Snapshot sync failed: {exc}\n"
            )


class SyncHistoryCommand:
    """
    Fetch committed history from server
    and store it into local HISTORY tables.
    """

    def GetResources(self):
        return {
            "MenuText": "Sync History",
            "ToolTip": "Sync committed history from server",
        }

    def IsActive(self):
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return

        try:
            # ✅ 1. Determine cursor locally
            from OPE_DB_API.db.session import get_client_db_session
            from OPE_DB_API.cache.metadata import get_last_history_id

            with get_client_db_session(provider.code) as db:
                last_id = get_last_history_id(db, provider.domain) or 0

            # ✅ 2. Fetch from server (PyDBML)
            rows = provider.fetch_history(after_history_id=last_id)

            # ✅ 3. Persist locally (OPETreeWB)
            apply_history(provider, rows)

            FreeCAD.Console.PrintMessage(
                f"✅ History synced ({len(rows)} rows)\n"
            )

        except Exception as exc:
            FreeCAD.Console.PrintError(
                f"❌ History sync failed: {exc}\n"
            )