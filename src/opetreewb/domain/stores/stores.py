from opetreewb.integration.opedbapi.core.context import OpeDBContext
OPE_DB_CONTEXT = OpeDBContext()

from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

ID_GENERATOR = SnowflakeIDGenerator()

from opetreewb.domain.services.attribute_service import AttributeService

ATT_SERVICE = AttributeService()

from opetreewb.domain.services.tree_service import TreeService

TREE_SERVICE = TreeService()

from opetreewb.domain.services.session_service import SessionService

SESSION_SERVICE = SessionService()