from datetime import datetime, timezone
from sqlalchemy import func

from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.models.session import SessionMetadata


def get_or_initialize_global_last_synced_at(
    *,
    code: str,
    active_session_id: int,
) -> datetime:
    """
    Return the global last_synced_at timestamp used for history sync.

    Behavior:
    - If any session has last_synced_at:
        → return MAX(last_synced_at)
    - If none exists (first-ever sync):
        → initialize last_synced_at = now() on the active session
        → return that same timestamp

    This function is:
    - idempotent
    - forward-only
    - safe to call on every Sync History click
    """

    with get_client_db_session(code) as db:
        # 1️⃣ Read global cursor
        last_ts = (
            db.query(func.max(SessionMetadata.last_synced_at))
            .scalar()
        )

        # 2️⃣ First-time sync: initialize baseline
        if last_ts is None:
            now_ts = datetime.now(tzinfo=timezone.utc)

            session = (
                db.query(SessionMetadata)
                .filter(SessionMetadata.session_id == active_session_id)
                .one_or_none()
            )

            if session is None:
                raise RuntimeError(
                    f"Active session {active_session_id} not found in local DB"
                )

            session.last_synced_at = now_ts
            db.commit()

            return now_ts

        # 3️⃣ Normal path
        return last_ts