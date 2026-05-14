from opetreewb.domain.services.attribute_service import AttributeService
from opetreewb.domain.services.geometry_service import GeometryService
from opetreewb.domain.services.session_service import SessionService
from opetreewb.domain.services.sync_service import SyncService
from opetreewb.domain.services.tree_service import TreeService
from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient


class ServiceContainer:
    """
    Central place to create and wire services.
    """

    def __init__(self):

        self.fcadclient = OpeDBClient()

        self.session_service = SessionService(fcadclient=self.fcadclient)

        # ✅ FIXED
        self.attribute_service = AttributeService(fcadclient=self.fcadclient)

        self.tree_service = TreeService(fcadclient=self.fcadclient)

        self.geometry_service = GeometryService()

        self.sync_service = SyncService(fcadclient=self.fcadclient)
