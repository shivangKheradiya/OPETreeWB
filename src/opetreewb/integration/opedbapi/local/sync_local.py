from opetreewb.integration.opedbapi.local.client import LocalClient
from OPE_DB_API.crud.live.read import get_live_row
from OPE_DB_API.crud.live.write import insert_live_row, update_live_row
from opetreewb.domain.stores.stores import OPE_DB_CONTEXT

class SyncLocal:
    def __init__(self,localclient:LocalClient=None):
        self.client = localclient
    
    def apply_snapshot(self, *, rows):
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