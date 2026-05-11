import FreeCAD
import FreeCADGui

from opetreewb.domain.services.service_locator import (
    get_session_service
)

class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return get_session_service().is_session_active()

    def Activated(self):
        get_session_service().commit()
        get_session_service().start()

class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return get_session_service().is_session_active()

    def Activated(self):
        get_session_service().abort()