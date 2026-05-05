import FreeCAD
import FreeCADGui

from opetreewb.infrastructure import SESSION_CONTEXT
from opetreewb.domain.session_service import SessionService

class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return True
        return SessionService().is_session_active()

    def Activated(self):
        service = SessionService()
        service.commit()
        service.start()

class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return True
        return SessionService().is_session_active()

    def Activated(self):
        service = SessionService()
        service.abort()