from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.cache.metadata import (
    get_last_history_id,
    set_last_history_id,
)
from OPE_DB_API.crud.history.write import write_history


def apply_history(provider, rows):
    """
    Persist history rows into local HISTORY tables.
    """

    domain = provider.domain
    code = provider.code

    with get_client_db_session(code) as db:
        last_id = get_last_history_id(db, domain) or 0

        for row in rows:
            write_history(db, domain, row)
            last_id = max(last_id, row["history_id"])

        set_last_history_id(db, domain, last_id)
        db.commit()