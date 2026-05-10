from opetreewb.integration.opedbapi.facade.opedb_client import OpeDBClient

from opetreewb.domain.services.session_service import SessionService
from opetreewb.domain.services.attribute_service import AttributeService
from opetreewb.domain.services.tree_service import TreeService
from opetreewb.domain.stores.stores import ID_GENERATOR


class ServiceContainer:
    """
    Central place to create and wire services.

    Handles dependency injection.
    """

    def __init__(self):

        self.opeclient = OpeDBClient(id_generator=ID_GENERATOR)

        self.session_service = SessionService(
            opeclient=self.opeclient
        )
        self.attribute_service = AttributeService()

        self.tree_service = TreeService(opeclient=self.opeclient)