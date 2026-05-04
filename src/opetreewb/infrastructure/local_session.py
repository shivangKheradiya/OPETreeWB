import FreeCAD

from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.crud.session.start import start_session
from OPE_DB_API.crud.session.query import validate_session_active
from OPE_DB_API.errors import SessionNotActiveError


def ensure_local_session(provider):
    """
    Ensure the currently active server session
    is registered in the local client database.

    This must be called immediately after
    provider.start_session().
    """

    session_id = provider._session_id
    if session_id is None:
        return

    with get_client_db_session(provider.code) as db:
        try:
            # ✅ Check if local session already exists
            validate_session_active(db, session_id=session_id)

            FreeCAD.Console.PrintMessage(
                f"[LocalSession] Local session {session_id} already exists\n"
            )
            return

        except SessionNotActiveError:
            # ✅ Create a local mirror of the session
            start_session(
                db,
                session_id=session_id,
                username=provider.username,
                hostname=provider.hostname,
                domain=provider.domain,
            )
            db.commit()

            FreeCAD.Console.PrintMessage(
                f"[LocalSession] Created local session {session_id}\n"
            )
