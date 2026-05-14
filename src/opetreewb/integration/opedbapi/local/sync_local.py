from datetime import datetime, timezone

from OPE_DB_API.crud.live.read import get_live_row
from OPE_DB_API.crud.live.write import (delete_live_row, insert_live_row,
                                        update_live_row)

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT
from opetreewb.integration.opedbapi.local.client import LocalClient


class SyncLocal:
    def __init__(self, localclient: LocalClient = None):
        self.client = localclient

    def apply_snapshot(self, rows):
        domain = OPE_DB_CONTEXT.domain.upper()
        db = self.client.get_session()

        try:
            for row in rows:
                existing = get_live_row(db, domain, row["data_id"])
                if existing:
                    update_live_row(db, existing, row["value"])
                else:
                    insert_live_row(db, domain, row)
            db.commit()
        finally:
            db.close()

    def sync_set_history(self, rows):
        latest_ts = None
        domain = OPE_DB_CONTEXT.domain.upper()
        db = self.client.get_session()
        try:
            for row in rows:
                row_ts = row.get("committed_at")

                if isinstance(row_ts, str):
                    row_ts = datetime.fromisoformat(row_ts)

                if row_ts.tzinfo is not None:
                    row_ts = row_ts.astimezone(timezone.utc).replace(tzinfo=None)

                if row_ts:
                    latest_ts = max(latest_ts, row_ts) if latest_ts else row_ts

                existing = get_live_row(db, domain, row["data_id"])

                op_type = row["operation_type"]

                payload = {
                    "data_id": row["data_id"],
                    "node_id": row["node_id"],
                    "attribute_id": row["attribute_id"],
                    "value": row.get("new_value", None),
                }

                if op_type == 1:  # CREATE / INSERT
                    if existing:
                        update_live_row(db, existing, row.get("new_value", None))
                    else:
                        insert_live_row(db, domain, payload)

                elif op_type == 2:  # UPDATE
                    if existing:
                        update_live_row(db, existing, row.get("new_value", None))

                elif op_type == 3:  # DELETE
                    if existing:
                        delete_live_row(db, existing)

            db.commit()
        finally:
            db.close()

        return latest_ts
