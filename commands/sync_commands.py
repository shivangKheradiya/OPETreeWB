import FreeCAD

from OPETreeWB.commands.session_commands import get_active_provider
from OPETreeWB.core.app_context import APP_CONTEXT

from OPETreeWB.core.sync.snapshot_sync import apply_snapshot
from OPETreeWB.core.cn_manager import CN
from OPETreeWB.core.sync.sync_cursor import (
    get_or_initialize_global_last_synced_at,
    update_last_synced_at_for_active_session,
)
from OPE_DB_API.db.session import get_client_db_session
from OPETreeWB.core.sync.history_replay import replay_history_rows

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
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("❌ No active provider\n")
            return

        if provider._session_id is None:
            FreeCAD.Console.PrintError("❌ No active session\n")
            return

        try:
            # ✅ 1. Resolve or initialize global history cursor
            after_ts = get_or_initialize_global_last_synced_at(
                code=provider.code,
                active_session_id=provider._session_id,
            )

            FreeCAD.Console.PrintMessage(
                f"ℹ️ History sync cursor = {after_ts.isoformat()}\n"
            )

            # ✅ 2. Fetch history from server (timestamp-based)
            rows = provider.fetch_history(after_ts=after_ts)

            FreeCAD.Console.PrintMessage(
                f"✅ History fetched ({len(rows)} rows)\n"
            )

            # ✅ 3. Apply history to LIVE tables (inside transaction)
            with get_client_db_session(provider.code) as db:
                replay_history_rows(
                    db=db,
                    domain=provider.domain,
                    history_rows=rows,
                )
                db.commit()

            FreeCAD.Console.PrintMessage(
                f"✅ History applied to LIVE ({len(rows)} rows)\n"
            )

            if rows:
                new_ts = max(
                    row["committed_at"]
                    for row in rows
                    if row.get("committed_at") is not None
                )

                update_last_synced_at_for_active_session(
                    code=provider.code,
                    session_id=provider._session_id,
                    new_ts=new_ts,
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
