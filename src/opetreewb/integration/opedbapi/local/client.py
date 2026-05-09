from sqlalchemy.orm import sessionmaker

from OPE_DB_API.db.engine import get_client_engine
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.bootstrap import initialize_opedb_config

class LocalClient:
    """
    Low-level local DB client.

    Responsibilities:
    - create engine using OPE_DB_API config
    - provide SQLAlchemy sessions
    """

    def __init__(self):

        # ✅ use project code from context
        code = OPE_DB_CONTEXT.code

        initialize_opedb_config()
        self.engine = get_client_engine(code)

        self.SessionFactory = sessionmaker(
            bind=self.engine,
            future=True
        )

    # -------------------------------------------------
    # SESSION ACCESS
    # -------------------------------------------------
    def get_session(self):
        """
        Returns new SQLAlchemy session
        """
        return self.SessionFactory()