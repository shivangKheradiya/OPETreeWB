from datetime import datetime
from sqlalchemy.orm import Session

from opetreewb.integration.opedbapi.core.operation_context import OperationContext

from opetreewb.integration.opedbapi.api.session_api import SessionAPI
from opetreewb.integration.opedbapi.api.node_api import NodeAPI
from opetreewb.integration.opedbapi.api.attribute_api import AttributeAPI
from opetreewb.integration.opedbapi.api.query_api import QueryAPI
from opetreewb.integration.opedbapi.api.client import OpeApiClient
from opetreewb.integration.opedbapi.api.sync_api import SyncAPI

from opetreewb.integration.opedbapi.local.session_local import SessionLocal
from opetreewb.integration.opedbapi.local.attribute_local import AttributeLocal
from opetreewb.integration.opedbapi.local.query_local import QueryLocal
from opetreewb.integration.opedbapi.local.client import LocalClient
from opetreewb.integration.opedbapi.local.node_local import NodeLocal
from opetreewb.integration.opedbapi.local.sync_local import SyncLocal

from opetreewb.domain.stores.stores import OPE_DB_CONTEXT,ID_GENERATOR
from opetreewb.messaging.reporter import Reporter

from OPE_DB_API.crud.commit.commit import commit_session
from OPE_DB_API.crud.session.abort import abort_session
from OPE_DB_API.crud.live.read import get_live_row
from OPE_DB_API.crud.live.write import insert_live_row, update_live_row

class OpeDBClient:
    """
    Hybrid client with explicit API / LOCAL separation.
    """

    def __init__(self):
        id_gen = ID_GENERATOR

        Reporter.info("[OpeDBClient] Initializing")

        self.operationcontext = OperationContext()

        # ✅ API
        self.api_client = OpeApiClient()
        self.api_session = SessionAPI()
        self.api_node = NodeAPI(id_generator=id_gen, op_context=self.operationcontext,opeapiclient=self.api_client)
        self.api_attr = AttributeAPI(id_generator=id_gen)
        self.api_query = QueryAPI()
        self.api_sync = SyncAPI()

        # ✅ LOCAL
        self.local_session = SessionLocal()
        self.local_attr = AttributeLocal(id_gen)
        self.local_query = QueryLocal()
        self.local_client = LocalClient()
        self.local_node = NodeLocal(op_context=self.operationcontext, localclient=self.local_client)
        self.local_sync = SyncLocal()

        Reporter.success("[OpeDBClient] Ready")

    # =========================================================
    # SESSION (EXPLICIT)
    # =========================================================

    # ---------- START ----------
    def start_session_api(self):
        Reporter.info("[OpeDBClient][API] start_session_api")
        try:
            session_id = self.api_session.start()
            Reporter.success(f"[OpeDBClient][API] session started → {session_id}")
            return session_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] start_session failed → {e}")
            raise

    def start_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] start_session_local")
        try:
            self.local_session.start()
            Reporter.success("[OpeDBClient][LOCAL] session created")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] start_session failed → {e}")
            raise

    # ---------- CLOSE ----------
    def close_session_api(self):
        Reporter.info("[OpeDBClient][API] close_session_api")
        try:
            session_id = self.api_session.close()
            Reporter.success("[OpeDBClient][API] session closed")
            return session_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] close_session failed → {e}")
            raise

    def close_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] close_session_local")
        try:
            self.local_session.close()
            Reporter.success("[OpeDBClient][LOCAL] session closed")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] close_session failed → {e}")
            raise

    # ---------- COMMIT ----------
    def commit_session_api(self):
        Reporter.info("[OpeDBClient][API] commit_session_api")
        try:
            result = self.api_client.post(
                "work/commit",
                use_session=True
            )
            Reporter.success("[OpeDBClient][API] commit applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] commit failed → {e}")
            raise

    def commit_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] commit_session_local")
        db: Session = self.local_client.get_session()
        try:
            commit_session(
                db,
                domain=OPE_DB_CONTEXT.domain.upper(),
                session_id=OPE_DB_CONTEXT.session_id,
            )
            db.commit()
            Reporter.success("[OpeDBClient][LOCAL] commit applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] commit failed → {e}")
            raise
        finally:
            db.close()

    # ---------- ABORT ----------
    def abort_session_api(self):
        Reporter.info("[OpeDBClient][API] abort_session_api")
        try:
            result = self.api_client.post(
                "work/discard",
                use_session=True
            )
            Reporter.success("[OpeDBClient][API] abort applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] abort failed → {e}")
            raise

    def abort_session_local(self):
        Reporter.info("[OpeDBClient][LOCAL] abort_session_local")

        db: Session = self.local_client.get_session()

        try:
            abort_session(
                db,
                session_id=OPE_DB_CONTEXT.session_id,
                domain=OPE_DB_CONTEXT.domain.upper(),
            )
            db.commit()
            Reporter.success("[OpeDBClient][LOCAL] abort applied")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] abort failed → {e}")
            raise
        finally:
            db.close()

    # =========================================================
    # ATTRIBUTE (EXPLICIT)
    # =========================================================

    def push_attribute_api(self, **kwargs):
        Reporter.info("[OpeDBClient][API] push_attribute_api")
        try:
            data_id = self.api_attr.push(**kwargs)
            Reporter.success(f"[OpeDBClient][API] attribute pushed → {data_id}")
            return data_id
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] push_attribute failed → {e}")
            raise

    def push_attribute_local(self, *, node_id, attribute_id, value, data_id):
        Reporter.info("[OpeDBClient][LOCAL] push_attribute_local")
        try:
            self.local_attr.push(
                node_id=node_id,
                attribute_id=attribute_id,
                value=value,
                data_id=data_id,
            )
            Reporter.success("[OpeDBClient][LOCAL] attribute stored")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] push_attribute failed → {e}")
            raise

    def delete_attribute_api(self, **kwargs):
        Reporter.info("[OpeDBClient][API] delete_attribute_api")
        try:
            self.api_attr.delete(**kwargs)
            Reporter.success("[OpeDBClient][API] attribute deleted")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] delete failed → {e}")
            raise

    def delete_attribute_local(self, **kwargs):
        Reporter.info("[OpeDBClient][LOCAL] delete_attribute_local")
        try:
            self.local_attr.delete(**kwargs)
            Reporter.success("[OpeDBClient][LOCAL] attribute removed")
        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] delete failed → {e}")
            raise

    # =========================================================
    # QUERY
    # =========================================================

    def search(self, **kwargs):

        Reporter.info("[OpeDBClient] SEARCH")

        try:
            Reporter.info("[OpeDBClient][LOCAL] search")
            result = self.local_query.search(**kwargs)

            if result and result.get("items"):
                Reporter.success("[OpeDBClient][LOCAL] result found")
                return result

            Reporter.info("[OpeDBClient][LOCAL] empty → fallback API")

        except Exception as e:
            Reporter.warning(f"[OpeDBClient][LOCAL] search failed → {e}")

        Reporter.info("[OpeDBClient][API] search fallback")

        try:
            result = self.api_query.search(**kwargs)
            Reporter.success("[OpeDBClient][API] result returned")
            return result
        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] search failed → {e}")
            raise

    def load_node(self, node_id):

        Reporter.info(f"[OpeDBClient] LOAD NODE → {node_id}")

        return self.search(
            filter_dict={
                "field": "node_id",
                "op": "=",
                "value": node_id,
            }
        )

    # =========================================================
    # NODE (API + LOCAL)
    # =========================================================
    def create_node_api(self, parent_node_id, element_type, name=None):
        Reporter.info("[OpeDBClient][API] create_node_api")
        try:
            node_id = self.api_node.create(
                parent_node_id=parent_node_id,
                type_value=element_type,
                name=name
            )

            Reporter.success(f"[OpeDBClient][API] node created → {node_id}")
            return node_id

        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] create_node failed → {e}")
            raise


    def create_node_local(self, parent_node_id, element_type, name=None):
        Reporter.info("[OpeDBClient][LOCAL] create_node_local")
        try:
            self.local_node.apply_operations()
            Reporter.success(f"[OpeDBClient][LOCAL] node created successfully.")

        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] create_node failed → {e}")
            raise


    # ---------- DELETE NODE ----------
    def delete_node_api(self, node_id, element_type):
        Reporter.info(f"[OpeDBClient][API] delete_node_api → {node_id}")

        try:
            self.api_node.delete(node_id, element_type)
            Reporter.success("[OpeDBClient][API] node deleted")

        except Exception as e:
            Reporter.error(f"[OpeDBClient][API] delete_node failed → {e}")
            raise


    def delete_node_local(self, node_id):
        Reporter.info(f"[OpeDBClient][LOCAL] delete_node_local → {node_id}")

        try:
            self.local_node.apply_operations()
            Reporter.success(f"[OpeDBClient][LOCAL] node deleted → {node_id}")

        except Exception as e:
            Reporter.error(f"[OpeDBClient][LOCAL] delete_node failed → {e}")
            raise

    def sync_get_snapshot_api(self, root_node_id, owner_attribute_id):
        return self.api_query.fetch_snapshot(root_node_id, owner_attribute_id)

    def sync_set_snapshot_local(self, rows):
        self.local_sync.apply_snapshot(rows)

    def sync_get_history_api(self, after_ts: datetime, limit: int = 5000):
        return self.api_query.fetch_history(after_ts=after_ts, limit=limit)

    def sync_set_history_local(self):
        pass

    def bootstrap_local(self, rows):
        session_id = OPE_DB_CONTEXT.session_id
        domain = OPE_DB_CONTEXT.domain.upper()
        db = self.local_client.get_session()
        try:
            for row in rows.get("items", []):
                existing = get_live_row(db, domain, row["data_id"])
                if existing:
                    update_live_row(db, existing, row["value"])
                else:
                    insert_live_row(db, domain, row)

            db.commit()
        finally:
            db.close()

    def fetch_root_nodes_api(self):
        return self.api_query.fetch_root_nodes()
    
    def get_root_nodes_local(self):
        return self.local_query.get_root_nodes()
    
    def get_children_local(self, parent_node_id):
        return self.local_query.get_children(parent_node_id)