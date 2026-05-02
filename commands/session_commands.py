# commands/session_commands.py
"""
Session control commands for PyDBML.

Provides:
- Start Session
- Commit Session
- Abort Session
"""

import FreeCAD
import FreeCADGui
from OPETreeWB.core.cn_manager import CN

# -------------------------------------------------
# GLOBAL PROVIDER HOLDER (temporary but correct)
# -------------------------------------------------

_active_provider = None


def set_active_provider(provider):
    """
    Set the active PyDBML provider for session commands.
    """
    global _active_provider
    _active_provider = provider


def get_active_provider():
    """
    Get the active PyDBML provider.
    """
    return _active_provider


# -------------------------------------------------
# COMMANDS
# -------------------------------------------------

class StartSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Start OPE Session",
            "ToolTip": "Start a PyDBML working session",
        }

    def IsActive(self):
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return

        try:
            provider.start_session()

            from OPETreeWB.data.local_session import ensure_local_session
            ensure_local_session(provider)

            set_active_provider(provider=provider)

            FreeCAD.Console.PrintMessage("OPE session started\n")
        except Exception as exc:
            FreeCAD.Console.PrintError(f"Failed to start session: {exc}\n")


class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return

        # ✅ Capture session_id BEFORE server commit
        session_id = provider._session_id
        if session_id is None:
            FreeCAD.Console.PrintError("No active session to commit\n")
            return

        domain = provider.domain
        code = provider.code

        try:
            # ✅ 1. SERVER COMMIT (authoritative)
            provider.commit()

            # ✅ 2. LOCAL COMMIT (mirror server success)
            from OPE_DB_API.db.session import get_client_db_session
            from OPE_DB_API.crud.commit.commit import commit_session

            with get_client_db_session(code) as db:
                commit_session(
                    db,
                    domain=domain,
                    session_id=session_id,
                )
                db.commit()

            CN(None)
            FreeCAD.Console.PrintMessage("✅ OPE session committed\n")

        except Exception as exc:
            FreeCAD.Console.PrintError(
                f"❌ Failed to commit session: {exc}\n"
            )


class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return get_active_provider() is not None

    def Activated(self):
        provider = get_active_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return
    
        # ✅ Capture session_id BEFORE server commit
        session_id = provider._session_id
        if session_id is None:
            FreeCAD.Console.PrintError("No active session to commit\n")
            return
    
        domain = provider.domain
        code = provider.code

        try:
            provider.abort()
            CN(None)  # ✅ clear current node
            from OPE_DB_API.crud.session.abort import abort_session
            from OPE_DB_API.db.session import get_client_db_session

            with get_client_db_session(provider.code) as db:
                abort_session(
                    db,
                    domain=domain,
                    session_id=session_id,
                )
                db.commit()
            FreeCAD.Console.PrintMessage("OPE session aborted\n")
        except Exception as exc:
            FreeCAD.Console.PrintError(f"Failed to abort session: {exc}\n")