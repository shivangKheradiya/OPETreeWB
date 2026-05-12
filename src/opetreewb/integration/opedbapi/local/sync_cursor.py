from datetime import datetime, timezone
from sqlalchemy import func
from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.models.session import SessionMetadata
from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT

def get_or_initialize_global_last_synced_at(
    *,
    localclient:LocalClient=None,
) -> datetime:
    active_session_id = OPE_DB_CONTEXT.session_id
    db = localclient.get_session()

    try:
        last_ts = db.query(func.max(SessionMetadata.last_synced_at)).scalar()

        if last_ts is None:
            now_ts = now_ts = datetime.now(timezone.utc).replace(tzinfo=None)

            session = (
                db.query(SessionMetadata)
                .filter(SessionMetadata.session_id == active_session_id)
                .one_or_none()
            )

            if session is None:
                raise RuntimeError(
                    f"Active session {active_session_id} not found"
                )

            session.last_synced_at = now_ts
            db.commit()

            last_ts = now_ts
    finally:
        db.close()

    return last_ts


def update_last_synced_at_for_active_session(
    *,
    localclient:LocalClient=None,
    new_ts: datetime,
) -> None:
    session_id = OPE_DB_CONTEXT.session_id
    db = localclient.get_session()

    try:
        session = (
            db.query(SessionMetadata)
            .filter(SessionMetadata.session_id == session_id)
            .one_or_none()
        )

        if session is None:
            raise RuntimeError(
                f"Active session {session_id} not found"
            )

        existing_ts = session.last_synced_at
        if existing_ts and existing_ts.tzinfo is not None:
            existing_ts = existing_ts.replace(tzinfo=None)
        if existing_ts is None or new_ts > existing_ts:
            session.last_synced_at = new_ts
            db.commit()
    finally:
        db.close()