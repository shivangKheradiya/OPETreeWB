import socket

from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT

from OPE_DB_API.crud.session.start import start_session
from OPE_DB_API.crud.session.close import close_session


class SessionLocal:
    """
    Local session management using OPE_DB_API CRUD.
    """

    def __init__(self):
        self.client = LocalClient()

    # -------------------------------------------------
    # START SESSION
    # -------------------------------------------------
    def start(self, session_id, username=None):

        db = self.client.get_session()

        try:
            hostname = OPE_DB_CONTEXT.hostname or socket.gethostname()

            session = start_session(
                db,
                session_id=session_id,
                username=username,
                hostname=hostname,
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
    def close(self, session_id):

        db = self.client.get_session()

        try:
            session = close_session(
                db,
                session_id=session_id
            )

            db.commit()
            db.refresh(session)
            return session

        finally:
            db.close()