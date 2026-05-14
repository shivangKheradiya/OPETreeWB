import socket

from OPE_DB_API.crud.session.close import close_session
from OPE_DB_API.crud.session.start import start_session

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.client import LocalClient


class SessionLocal:
    """
    Local session management using OPE_DB_API CRUD.
    """

    def __init__(self):
        self.client = LocalClient()

    # -------------------------------------------------
    # START SESSION
    # -------------------------------------------------
    def start(self):

        db = self.client.get_session()

        try:
            session = start_session(
                db,
                session_id=OPE_DB_CONTEXT.session_id,
                username=OPE_DB_CONTEXT.username,
                hostname=OPE_DB_CONTEXT.hostname,
                domain=OPE_DB_CONTEXT.domain,
            )

            db.commit()
            db.refresh(session)

            return session

        finally:
            db.close()

    # -------------------------------------------------
    # CLOSE SESSION
    # -------------------------------------------------
    def close(self):

        db = self.client.get_session()

        try:
            session = close_session(db, session_id=OPE_DB_CONTEXT.session_id)

            db.commit()
            db.refresh(session)
            return session

        finally:
            db.close()
