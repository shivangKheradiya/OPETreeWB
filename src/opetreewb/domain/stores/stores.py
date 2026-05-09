from opetreewb.integration.opedbapi.core.context import OpeDBContext
OPE_DB_CONTEXT = OpeDBContext()

from opetreewb.domain.identity.snowflake import SnowflakeIDGenerator

ID_GENERATOR = SnowflakeIDGenerator()
