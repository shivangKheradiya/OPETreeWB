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

        try:
            provider.commit()
            FreeCAD.Console.PrintMessage("OPE session committed\n")
        except Exception as exc:
            FreeCAD.Console.PrintError(f"Failed to commit session: {exc}\n")


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

        try:
            provider.abort()
            FreeCAD.Console.PrintMessage("OPE session aborted\n")
        except Exception as exc:
            FreeCAD.Console.PrintError(f"Failed to abort session: {exc}\n")