import FreeCAD
import FreeCADGui

from opetreewb.infrastructure import SESSION_CONTEXT
from opetreewb.domain.stores.stores import SESSION_SERVICE

class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return SESSION_SERVICE.is_session_active()

    def Activated(self):
        service = SESSION_SERVICE
        service.commit()
        service.start()

class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return SESSION_SERVICE.is_session_active()

    def Activated(self):
        service = SESSION_SERVICE
        service.abort()