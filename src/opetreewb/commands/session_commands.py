import FreeCAD
import FreeCADGui

from opetreewb.infrastructure import SESSION_CONTEXT


def StartSession():
    provider = SESSION_CONTEXT.get_provider()

    try:
        FreeCAD.Console.PrintMessage("✅ OPE session started\n")
    except Exception as exc:
        FreeCAD.Console.PrintError(
            f"Failed to start session: {exc}\n"
        )

def CommitSession():
    provider = SESSION_CONTEXT.get_provider()
    try:
        FreeCAD.Console.PrintMessage("✅ OPE session committed\n")
    except Exception as exc:
        FreeCAD.Console.PrintError(
            f"❌ Failed to commit session: {exc}\n"
        )

def AbortSession():
    provider = SESSION_CONTEXT.get_provider()

    try:
        FreeCAD.Console.PrintMessage("✅ OPE session aborted\n")
    except Exception as exc:
        FreeCAD.Console.PrintError(f"❌ Failed to abort session: {exc}\n")


class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return SESSION_CONTEXT.IsSessionLive()

    def Activated(self):
        CommitSession()
        StartSession()

class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return SESSION_CONTEXT.IsSessionLive()

    def Activated(self):
        AbortSession()