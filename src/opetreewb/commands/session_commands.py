import FreeCAD
import FreeCADGui

from opetreewb.infrastructure import SESSION_CONTEXT
from opetreewb.infrastructure.local_session import ensure_local_session


class StartSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Start OPE Session",
            "ToolTip": "Start a working session",
        }

    def IsActive(self):
        provider = SESSION_CONTEXT.get_provider()
        return provider is not None

    def Activated(self):
        provider = SESSION_CONTEXT.get_provider()
        if provider is None:
            FreeCAD.Console.PrintError("No active provider\n")
            return

        try:
            provider.start_session()
            ensure_local_session(provider)

            # ✅ authoritative session location
            SESSION_CONTEXT.set_provider(provider)

            FreeCAD.Console.PrintMessage("OPE session started\n")

        except Exception as exc:
            FreeCAD.Console.PrintError(
                f"Failed to start session: {exc}\n"
            )