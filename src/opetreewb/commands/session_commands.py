import FreeCAD
import FreeCADGui

from opetreewb.app.app_context import AppContext
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT, ID_GENERATOR

class CommitSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Commit OPE Session",
            "ToolTip": "Commit current PyDBML session",
        }

    def IsActive(self):
        return AppContext.container.session_service.is_session_active()

    def Activated(self):
        service = AppContext.container.session_service
        service.commit()
        service.start()

class AbortSessionCommand:
    def GetResources(self):
        return {
            "MenuText": "Abort OPE Session",
            "ToolTip": "Abort current PyDBML session",
        }

    def IsActive(self):
        return AppContext.container.session_service.is_session_active()

    def Activated(self):
        service = AppContext.container.session_service
        service.abort()