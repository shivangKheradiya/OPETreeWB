from OPE_DB_API.db.session import get_client_db_session
from OPE_DB_API.crud.live.read import get_live_row
from OPE_DB_API.crud.live.write import insert_live_row, update_live_row


def apply_snapshot(provider, rows):
    """
    Persist snapshot rows into local LIVE tables.
    """

    domain = provider.domain
    code = provider.code

    with get_client_db_session(code) as db:
        for row in rows:
            existing = get_live_row(db, domain, row["data_id"])
            if existing:
                update_live_row(db, existing, row["value"])
            else:
                insert_live_row(db, domain, row)

        db.commit()